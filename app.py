from secrets import token_hex
from random import sample
from time import time
from flask import (
    Flask,
    redirect,
    send_file,
    render_template
)
from flask_socketio import (
    emit,
    SocketIO,
    join_room
)

it = ["1B", "1C", "1D", "1S", "2B", "2C", "2D", "2S", "3B", "3C", "3D", "3S", "4B", "4C", "4D", "4S", "5B", "5C", "5D", "5S", "6B", "6C", "6D", "6S", "7B", "7C", "7D", "7S", "8B", "8C", "8D", "8S", "9B", "9C", "9D", "9S", "10B", "10C", "10D", "10S"]
fr = ["1C", "1F", "1P", "1Q", "2C", "2F", "2P", "2Q", "3C", "3F", "3P", "3Q", "4C", "4F", "4P", "4Q", "5C", "5F", "5P", "5Q", "6C", "6F", "6P", "6Q", "7C", "7F", "7P", "7Q", "8C", "8F", "8P", "8Q", "9C", "9F", "9P", "9Q", "10C", "10F", "10P", "10Q", "JC", "JF", "JP", "JQ", "QC", "QF", "QP", "QQ", "KC", "KF", "KP", "KQ", "BJ", "RJ"]

app = Flask(__name__)
app.secret_key = token_hex(16)
app.template_folder = "templates/min"
socketio = SocketIO(app)

@app.get("/")
@app.get("/<room>")
def index(room = None):
    if room is None:
        return render_template("index.min.html", room = int(time()), start = True, it = sample(it, 40), fr = sample(fr, 54))
    else:
        return render_template("index.min.html", room = room)

@socketio.on("join")
def join(data):
    join_room(data["room"])

@socketio.on("table")
def table(data):
    emit("table", {"table": data["table"]}, room = data["room"])

@app.route("/robots.txt")
def robots():
    return send_file("robots.txt")

@app.route("/sitemap.xml")
def sitemap():
    return send_file("sitemap.xml")

# @app.route("/manifest.json")
# def manifest():
#     return send_file("manifest.json")

# @app.route("/service-worker.js")
# def service_worker():
#     return send_file("service-worker.js")

@app.errorhandler(404)
@app.errorhandler(405)
def error(_):
    return redirect("/")

if __name__ == "__main__": socketio.run(app, debug = True)