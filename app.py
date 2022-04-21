"""Game Recommendation App"""
import os
import flask
from flask_login import (
    LoginManager,
    login_required,
    current_user,
    login_user,
    logout_user,
)
from dotenv import find_dotenv, load_dotenv
import flask_login
from steamspy import querygames, query_favorites
from models import Favorite, db, User, Survey


load_dotenv(find_dotenv())
login_manager = LoginManager()
game_list = {}
reviews = []

app = flask.Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
db_url = os.getenv("DATABASE_URL")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


db.init_app(app)

login_manager.login_view = "login"
login_manager.init_app(app)


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    """loads user"""
    return User.query.get(int(user_id))


@app.route("/login", methods=["POST", "GET"])
def login():
    """Route which handles user login"""
    if flask.request.method == "POST":
        email = flask.request.form["email"]
        password = flask.request.form["password"]
        user = User.query.filter_by(email=email).first()
        # If user exists, login. If not, flash error
        if user and user.verify_password(password):
            login_user(user)
            return flask.redirect(flask.url_for("main"))
        error = "User does not exist or password is incorrect."
        return flask.render_template("login.html", error=error)
    # GET route
    return flask.render_template("login.html")


@app.route("/logout", methods=["POST"])
def logout():
    """Route that handles user logout"""
    logout_user()
    return flask.redirect(flask.url_for("login"))


@app.route("/signup", methods=["POST", "GET"])
def signup():
    """Route that handles a user registration to the site"""
    # Captures information from form
    if flask.request.method == "POST":
        email = flask.request.form["email"]
        username = flask.request.form["username"]
        password = flask.request.form["password"]
        # Restricts email from being too long(Max Length: 64 characters)
        if len(email) > 64:
            error = "Length of email is too long."
            return flask.render_template("signup.html", error=error)
        # Similar process as previous if statement for username and password
        elif len(username) > 24:
            error = "Length of username is too long."
            return flask.render_template("signup.html", error=error)
        elif len(password) > 128:
            error = "Length of password is too long."
            return flask.render_template("signup.html", error=error)
        if len(email.strip()) >= 3:
            user = User(username, email, password)
            existing = User.query.filter_by(email=email).all()
            if not existing:
                # Add user if email isnt taken
                db.session.add(user)
                db.session.commit()
                user = User.query.filter_by(email=email).first()
                login_user(user)
                return flask.redirect(flask.url_for("survey"))
            # If taken, flash error
            error = "email already exists!"
        else:
            # If empty email, flash error
            error = "Empty emails are not allowed!"
        # Redirect to signup if any errors
        return flask.render_template("signup.html", error=error)
    # GET route
    return flask.render_template("signup.html")


@app.route("/gamepage", methods=["POST", "GET"])
@login_required
def gamepage():
    """Route which renders the page that displays information like price, reviews, etc about the game."""
    # If a user adds a favorite using the button on a game page, take him to their favorites page
    if flask.request.method == "POST":
        return flask.redirect(flask.url_for("favorites"))
    # Acquire game information from site parameters
    image = flask.request.args.get("image")
    title = flask.request.args.get("title")
    gameid = int(flask.request.args.get("gameid"))
    price = flask.request.args.get("price")
    # Check to see if this game is already favorited by the user - Depending on if it is or not, render the button in a different way.
    favorite = Favorite.query.filter_by(
        username=flask_login.current_user.username, gameid=gameid
    ).first()
    if favorite:
        message = "Remove from Favorites"
        color = "White"
    else:
        message = "Add to Favorites"
        color = "red"
    # Set price
    if price != "FREE":
        price = int(price) / 100
    price = int(flask.request.args.get("price")) / 100
    for game in game_list:
        if game["title"] == title:
            global reviews
            reviews = game["reviews"]
    if price == 0.0:
        price = 0
    return flask.render_template(
        "gamepage.html",
        title=title,
        price=price,
        image=image,
        gameid=gameid,
        message=message,
        color=color,
        reviews=reviews,
        len=len(reviews),
    )


@app.route("/favorite", methods=["POST", "GET"])
@login_required
def favorite():
    """Route to add or remove a game from favorites"""
    # Takes API fetch call and stores the relevant game id in favorite_data
    favorite_data = flask.request.get_json()
    # If game is already in favorites, remove the game from favorites, and vice versa.
    favorite = Favorite.query.filter_by(
        username=flask_login.current_user.username, gameid=favorite_data
    ).first()
    if favorite:
        db.session.delete(favorite)
    else:
        new_favorite = Favorite(
            username=flask_login.current_user.username, gameid=favorite_data
        )
        db.session.add(new_favorite)
    db.session.commit()
    return flask.redirect(flask.url_for("favoritespage"))


@app.route("/favoritespage", methods=["POST", "GET"])
@login_required
def favoritespage():
    """Route that handles loading the favorited games of the users"""
    # Acquire IDs of favorited games
    fav_ids = []
    favorite_list = Favorite.query.filter_by(
        username=flask_login.current_user.username
    ).all()
    for fav in favorite_list:
        fav_ids.append(fav.gameid)
    # Use query_favorites to attain information about those games
    fav_games = query_favorites(fav_ids)
    return flask.render_template(
        "favorites.html", length=len(fav_games), games=fav_games
    )


@app.route("/main", methods=["POST", "GET"])
@login_required
def main():
    """Route that handles generating a users recommendations given their survey data."""
    # Pull survey data from DB
    userid = current_user.id
    survey_data = Survey.query.filter_by(user_id=userid).first()

    # Use querygames to generate recommendations with survey data
    if survey_data:
        games = querygames(survey_data)
        global game_list
        game_list = games
        return flask.render_template("main.html", len=len(games), games=games,)
    return flask.redirect(flask.url_for("survey"))


@app.route("/", methods=["POST", "GET"])
def landing():
    """Landing Page"""
    return flask.render_template("landing.html")


@app.route("/survey", methods=["POST", "GET"])
@login_required
def survey():
    """Route will handle and store survey data"""
    # After user takes survey, store it into the DB
    if flask.request.method == "POST":
        userid = current_user.id
        Survey.query.filter_by(user_id=userid).delete()
        action = flask.request.form["action"]
        adventure = flask.request.form["adventure"]
        roleplaying = flask.request.form["roleplaying"]
        strategy = flask.request.form["strategy"]
        sports = flask.request.form["sports"]
        simulation = flask.request.form["simulation"]
        racing = flask.request.form["racing"]
        survey_data = Survey(
            user=userid,
            action=action,
            adventure=adventure,
            roleplaying=roleplaying,
            strategy=strategy,
            sports=sports,
            simulation=simulation,
            racing=racing,
        )
        db.session.add(survey_data)
        db.session.commit()
        return flask.redirect(flask.url_for("main"))

    return flask.render_template("survey.html")


@app.route("/profile")
@login_required
def profile():
    """Route that handles generating a users profile."""
    userid = current_user.id
    survey_data = Survey.query.filter_by(user_id=userid).first()
    # Pull survey data and use on profile
    if survey_data:
        user_name = current_user.username
        email = current_user.email
        action = survey_data.action
        adventure = survey_data.adventure
        roleplaying = survey_data.roleplaying
        strategy = survey_data.strategy
        sports = survey_data.sports
        simulation = survey_data.simulation
        racing = survey_data.racing
        return flask.render_template(
            "profile.html",
            email=email,
            user_name=user_name,
            action=action,
            adventure=adventure,
            roleplaying=roleplaying,
            strategy=strategy,
            sports=sports,
            simulation=simulation,
            racing=racing,
        )
    return flask.redirect(flask.url_for("survey"))


if __name__ == "__main__":
    app.run(
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", "8080")),
        debug=False,
    )
