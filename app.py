from time import time
from os import listdir
from random import sample
from secrets import token_hex
from cryptography.fernet import Fernet
from flask_socketio import emit, SocketIO, join_room
from flask import Flask, request, redirect, send_file, render_template

fernet_obj = Fernet(Fernet.generate_key())
encrypted_ita_deck = [fernet_obj.encrypt(card.encode()).decode() for card in listdir("static/assets/decks/ita")]
encrypted_fr1_deck = [fernet_obj.encrypt(card.encode()).decode() for card in listdir("static/assets/decks/fr1")]
encrypted_fr2_deck = [fernet_obj.encrypt(card.encode()).decode() for card in listdir("static/assets/decks/fr2")]

app = Flask(__name__)
socketio = SocketIO(app)
app.secret_key = token_hex(16)

@app.get("/")
@app.get("/<int(fixed_digits=10):room>")
def index(room = None):
    if room is None:
        return render_template(
            "index.html",
            room = int(time()),
            host = True,
            ita_deck = sample(encrypted_ita_deck, 40),
            fr1_deck = sample(encrypted_fr1_deck, 54),
            fr2_deck = sample(encrypted_fr2_deck, 54)
        )
    else:
        return render_template("index.html", room = room)

@socketio.on("join")
def handle_join(data):
    join_room(data["room"])

@socketio.on("play")
def handle_play(data):
    emit("play", {"table": data["table"]}, to = data["room"])
    emit("chat", {"message": f"BOT: {data["nick"]} ha mosso/pescato"}, to = data["room"])

@socketio.on("turn")
def handle_turn(data):
    emit("turn", {"value": fernet_obj.decrypt(data["card"]).decode(), "card": data["card"]}, to = data["room"])

@socketio.on("chat")
def handle_chat(data):
    emit("chat", {"message": f"{data["nick"]}: {data["message"]}"}, to = data["room"])

@app.get("/robots.txt")
@app.get("/sitemap.xml")
@app.get("/manifest.json")
@app.get("/service-worker.js")
@app.get("/.well-known/assetlinks.json")
def serve_file():
    return send_file(f"./{request.path}")

@app.errorhandler(404)
@app.errorhandler(405)
def error(_):
    return redirect("/")

if __name__ == "__main__": app.run(debug = True)