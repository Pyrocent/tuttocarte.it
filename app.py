from time import time
from os import listdir
from random import sample
from secrets import token_hex
from cryptography.fernet import Fernet
from flask_socketio import emit, SocketIO, join_room
from flask import Flask, request, redirect, send_file, render_template

fernet_obj = Fernet(Fernet.generate_key())
encrypted_ita_deck = [fernet_obj.encrypt(card.encode()).decode().replace("==", "") for card in listdir("static/assets/decks/ita")]
encrypted_fr1_deck = [fernet_obj.encrypt(card.encode()).decode().replace("==", "") for card in listdir("static/assets/decks/fr1")]
encrypted_fr2_deck = [fernet_obj.encrypt(card.encode()).decode().replace("==", "") for card in listdir("static/assets/decks/fr2")]

app = Flask(__name__)
socketio = SocketIO(app)
app.secret_key = token_hex(16)

@app.get("/")
@app.get("/<int(fixed_digits=10):room>")
def start(room = False):
    if not room: return redirect(f"/{int(time())}")
    return render_template(
        "index.html",
        room = room,
        ita_deck = sample(encrypted_ita_deck, 40),
        fr1_deck = sample(encrypted_fr1_deck, 54),
        fr2_deck = sample(encrypted_fr2_deck, 54)
    )

@socketio.on("join")
def handle_join(data):
    join_room(data["room"])
    emit("join", {"user": request.sid}, to = data["room"], include_self = False)

@socketio.on("play")
def handle_play(data): emit("play", {"html": data["html"]}, to = data.get("user", data["room"]), include_self = False)

@socketio.on("turn")
def handle_turn(data): emit("turn", {"id": data["id"], "value": fernet_obj.decrypt(data["id"] + "==").decode()}, to = data.get("room", request.sid))
    
@socketio.on("hand")
def handle_hand(data): emit("hand", {"html": data["html"], "hand": {"top": data["hand"]["top"], "left": data["hand"]["left"]}}, to = data["room"], include_self = False)

@app.get("/robots.txt")
@app.get("/sitemap.xml")
@app.get("/manifest.json")
@app.get("/service-worker.js")
@app.get("/.well-known/assetlinks.json")
def serve_file(): return send_file(f"./{request.path}")

@app.errorhandler(404)
@app.errorhandler(405)
def error(_): return redirect("/")

if __name__ == "__main__": socketio.run(app)