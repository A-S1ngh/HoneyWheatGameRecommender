import flask
import os
import requests
from flask_sqlalchemy import SQLAlchemy
from dotenv import find_dotenv, load_dotenv
from steamspy import querygames
from models import User, Survey, db


load_dotenv(find_dotenv())
# database still need to be connected to a heroku url
app = flask.Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/", methods=["POST", "GET"])
def login():
    """ "login"""
    users = Survey.query.all()
    print(users)
    querygames()
    return flask.render_template("index.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    """signup"""
    return flask.render_template("signup.html")


@app.route("/survey", methods=["POST", "GET"])
def survey():
    """Survey"""
    return flask.render_template("survey.html")


if __name__ == "__main__":
    app.run(
        host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True
    )
