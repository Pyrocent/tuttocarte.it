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
encrypted_ita_deck = [Fernet(encryption_key).encrypt(card.encode()).decode() for card in listdir("static/assets/decks/ita")]
encrypted_fr1_deck = [Fernet(encryption_key).encrypt(card.encode()).decode() for card in listdir("static/assets/decks/fr1")]
encrypted_fr2_deck = [Fernet(encryption_key).encrypt(card.encode()).decode() for card in listdir("static/assets/decks/fr2")]

app = Flask(__name__)
socket = SocketIO(app)
app.secret_key = token_hex(16)
app.template_folder = "templates/min"

@app.get("/")
@app.get("/<room>")
def index(room = None):
    if room is not None:
        return render_template("index.min.html", room = room)

    return render_template(
        "index.min.html",
        room = int(time()),
        host = True,
        ita_deck = sample(encrypted_ita_deck, 40),
        fr1_deck = sample(encrypted_fr1_deck, 54),
        fr2_deck = sample(encrypted_fr2_deck, 54)
    )

@socket.on("join")
def join(data):
    join_room(data["room"])

@socket.on("play")
def play(data):
    emit("play", {"table": data["table"]}, to = data["room"])

@socket.on("move")
def move(data):
    emit("move", {"card": data["card"]}, to = data["room"])

@socket.on("turn")
def turn(data):
    emit("turn", {"value": Fernet(encryption_key).decrypt(data["card"]).decode()}, to = data["room"])

@socket.on("hand")
def hand(data):
    emit("hand", {"card": data["card"]}, to = data["room"])

@socket.on("chat")
def chat(data):
    emit("chat", {"chat": data["chat"]}, to = data["room"])

@app.route("/robots.txt")
def robots():
    return send_file("robots.txt")

@app.route("/sitemap.xml")
def sitemap():
    return send_file("sitemap.xml")

@app.route("/manifest.json")
def manifest():
    return send_file("manifest.json")

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