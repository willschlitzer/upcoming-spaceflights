from flask import Flask

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return "<h1>Upcoming Spaceflights</h1><p>This site is an API for returning data about upcoming spaceflights</p>"


if __name__ == "__main__":
    app.run(debug=True)
