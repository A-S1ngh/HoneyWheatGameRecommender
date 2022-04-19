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
from steamspy import querygames
from models import Favorite, db, User, Survey


load_dotenv(find_dotenv())
login_manager = LoginManager()

# database still need to be connected to a heroku url

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
    """login"""
    if flask.request.method == "POST":
        email = flask.request.form["email"]
        password = flask.request.form["password"]
        user = User.query.filter_by(email=email).first()
        # If user exists, login. If not, flash error
        if user and user.verify_password(password):
            login_user(user)
            return flask.redirect(flask.url_for("main"))
        flask.flash("User does not exist!")
    # GET route
    return flask.render_template("login.html")


@app.route("/logout", methods=["POST"])
def logout():
    """logout user"""
    logout_user()
    return flask.redirect(flask.url_for("login"))


@app.route("/signup", methods=["POST", "GET"])
def signup():
    """signup"""
    if flask.request.method == "POST":
        email = flask.request.form["email"]
        username = flask.request.form["username"]
        password = flask.request.form["password"]
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
            flask.flash("email already exists!")
        else:
            # If empty email, flash error
            flask.flash("Empty emails are not allowed!")
        # Redirect to signup if any errors
        return flask.redirect(flask.url_for("signup"))
    # GET route
    return flask.render_template("signup.html")


@app.route("/gamepage", methods=["POST", "GET"])
@login_required
def gamepage():
    """gamepage"""
    if flask.request.method == "POST":
        return flask.redirect(flask.url_for("favorites"))
    image = flask.request.args.get("image")
    title = flask.request.args.get("title")
    gameid = int(flask.request.args.get("gameid"))
    price = flask.request.args.get("price")
    favorite = Favorite.query.filter_by(
        username=flask_login.current_user.username, gameid=gameid
    ).first()
    if favorite:
        message = "Remove from Favorites"
        color = "White"
    else:
        message = "Add to Favorites"
        color = "red"
    if price != "FREE":
        price = int(price) / 100
    return flask.render_template(
        "gamepage.html",
        title=title,
        price=price,
        image=image,
        gameid=gameid,
        message=message,
        color=color,
    )


@app.route("/favorite", methods=["POST"])
@login_required
def favorite():
    """Route to add or remove a game from favorites"""
    favorite_data = flask.request.get_json()
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


@app.route("/favoritespage", methods=["POST", "GET"])
@login_required
def favoritespage():
    return flask.render_template("favorites.html")


@app.route("/", methods=["POST", "GET"])
@login_required
def main():
    """main"""
    userid = current_user.id
    survey_data = Survey.query.filter_by(user_id=userid).first()
    if survey_data:
        games = querygames(survey_data)
        return flask.render_template("main.html", len=len(games), games=games,)
    return flask.redirect(flask.url_for("survey"))


@app.route("/survey", methods=["POST", "GET"])
@login_required
def survey():
    """Survey"""
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
    """User Profile"""
    userid = current_user.id
    survey_data = Survey.query.filter_by(user_id=userid).first()
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


if __name__ == "__main__":
    app.run(
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", "8080")),
        debug=False,
    )
