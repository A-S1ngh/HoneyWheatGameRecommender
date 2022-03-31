import flask

app = flask.Flask(__name__)


@app.route("/")
def login():
    return flask.render_template("index.html")
