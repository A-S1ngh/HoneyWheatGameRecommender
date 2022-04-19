from turtle import title
import flask
from flask_login import (
    LoginManager,
    login_required,
    current_user,
    login_user,
    logout_user,
)

import os
import requests
from flask_sqlalchemy import SQLAlchemy
from dotenv import find_dotenv, load_dotenv
from steamspy import querygames
from models import db, User, Survey


load_dotenv(find_dotenv())
login_manager = LoginManager()

# database still need to be connected to a heroku url
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

login_manager.login_view = "index"
login_manager.init_app(app)


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/", methods=["POST", "GET"])
def login():
    """login"""
    if flask.request.method == "POST":
        email = flask.request.form["email"]
        password = flask.request.form["password"]
        user = User.query.filter_by(email=email).first()
        # If user exists, login. If not, flash error
        if user and user.verify_password(password):
            login_user(user)
            print("WORKS")
            return flask.redirect(flask.url_for("survey"))
        flask.flash("User does not exist!")
    # GET route
    return flask.render_template("index.html")


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

def set(game):
    reviews.append(game) 
@login_required
@app.route("/gamepage", methods=["POST", "GET"])
def gamepage():
    """gamepage"""
    print(current_user)
    print(current_user.email)
    image = flask.request.args.get("image")
    title = flask.request.args.get("title")
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
        reviews=reviews,
        len=len(reviews),
    )


@login_required
@app.route("/main", methods=["POST", "GET"])
def main():
    """main"""
    userid = current_user.id
    survey_data = Survey.query.filter_by(user_id=userid).first()
    games = querygames(survey_data, userid)
    global game_list
    game_list = games
    
    return flask.render_template(
        "main.html",
        len=len(games),
        games=games,
    )


@login_required
@app.route("/survey", methods=["POST", "GET"])
def survey():
    """Survey"""
    userid = current_user.id
    survey_data = Survey.query.filter_by(user_id=userid).first()
    if survey_data:
        return flask.redirect(flask.url_for("main"))

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
        print(User.survey_data)
        return flask.redirect(flask.url_for("main"))

    return flask.render_template("survey.html")


@login_required
@app.route("/profile")
def profile():
    """User Profile"""
    userid = current_user.id
    survey_data = Survey.query.filter_by(user_id=userid).first()
    print(survey_data.action)
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
        host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=False
    )
