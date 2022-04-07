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
from models import User, Survey, db


load_dotenv(find_dotenv())
login_manager = LoginManager()

# database still need to be connected to a heroku url
app = flask.Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
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


@app.route("/", methods=["POST", "GET"])
def login():
    """ "login"""
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

@login_required
@app.route("/survey", methods=["POST", "GET"])
def survey():
    """Survey"""
    return flask.render_template("survey.html")

@login_required
@app.route("/profile")
def profile():
    """User Profile"""
    return flask.render_template("profile.html")


if __name__ == "__main__":
    app.run(
        host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True
    )
