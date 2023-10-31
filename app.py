from cryptography.fernet import Fernet
from secrets import token_hex
from random import sample
from os import listdir
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

encryption_key = Fernet.generate_key()
encrypted_italian_deck = [Fernet(encryption_key).encrypt(card.encode()).decode() for card in listdir("static/assets/decks/italian")]
encrypted_french_deck = [Fernet(encryption_key).encrypt(card.encode()).decode() for card in listdir("static/assets/decks/french")]

app = Flask(__name__)
app.secret_key = token_hex(16)
app.template_folder = "templates/min"
socket = SocketIO(app)

@app.get("/")
@app.get("/<room>")
def index(room = None):
    if room is not None:
        return render_template("index.min.html", room = room)

    return render_template(
        "index.min.html",
        room = int(time()),
        host = True,
        italian_deck = sample(encrypted_italian_deck, 40),
        french1_deck = sample(encrypted_french_deck, 54),
        french2_deck = sample(encrypted_french_deck, 54)
    )

@socket.on("join")
def join(data):
    join_room(data["room"])

@socket.on("draw")
def draw(data):
    emit("draw", {"card": Fernet(encryption_key).decrypt(data["id"]).decode()}, room = data["user"])

@socket.on("table")
def table(data):
    emit("table", {"html": data["html"]}, room = data["room"])

@socket.on("notes")
def notes(data):
    emit("notes", {"notes": data["notes"]}, room = data["room"])

@app.route("/ads.txt")
def ads():
    return send_file("ads.txt")

@app.route("/robots.txt")
def robots():
    return send_file("robots.txt")

@app.route("/sitemap.xml")
def sitemap():
    return send_file("sitemap.xml")

@app.route("/app.webmanifest")
def manifest():
    return send_file("app.webmanifest")

@app.route("/service-worker.js")
def service_worker():
    return send_file("service-worker.js")

@app.route("/.well-known/assetlinks.json")
def assetlinks():
    return send_file(".well-known/assetlinks.json")

@app.errorhandler(404)
@app.errorhandler(405)
def error(_):
    return redirect("/")

if __name__ == "__main__": socket.run(app, allow_unsafe_werkzeug = True)