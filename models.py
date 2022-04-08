from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), nullable=False)
    email = db.Column(db.String(24), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    survey_data = db.relationship("Survey", backref="user", uselist=False)

    def __repr__(self):
        return f"<User {self.email}>"

    def __init__(self, username, email, password):
        self.email = email
        self.username = username
        self.password = generate_password_hash(password)
    
    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)


class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    action = db.Column(db.Integer)
    adventure = db.Column(db.Integer)
    roleplaying = db.Column(db.Integer)
    strategy = db.Column(db.Integer)
    sports = db.Column(db.Integer)
    simulation = db.Column(db.Integer)
    racing = db.Column(db.Integer)

    def __init__(
        self, action, adventure, roleplaying, strategy, sports, simulation, racing, user
    ):
        self.action = action
        self.adventure = adventure
        self.roleplaying = roleplaying
        self.strategy = strategy
        self.sports = sports
        self.simulation = simulation
        self.racing = racing
        self.user_id = user