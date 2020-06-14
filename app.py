from flask import Flask
from scraper import get_time
from update_time import check_file

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    #cur_time = str(get_time())
    update = check_file()
    if update:
        upd_string = "Time to update!"
    else:
        upd_string = "Not now"
    return "<h1>Upcoming Spaceflights</h1><p>This site is an API for returning data about upcoming spaceflights<br/>" + upd_string + "</p>"


if __name__ == "__main__":
    app.run(debug=True)
