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
def start():
    return render_template("index.html", ita_deck = sample(encrypted_ita_deck, 40), fr1_deck = sample(encrypted_fr1_deck, 54),fr2_deck = sample(encrypted_fr2_deck, 54))

@socketio.on("join")
def handle_join(_):
    join_room(request.remote_addr)
    emit("join", {"user": request.sid}, to = request.remote_addr, include_self = False)

@socketio.on("play")
def handle_play(data): emit("play", {"html": data["html"]}, to = data.get("user", request.remote_addr), include_self = False)

@socketio.on("turn")
def handle_turn(data): emit("turn", {"id": data["id"], "value": fernet_obj.decrypt(data["id"] + "==").decode()}, to = request.remote_addr)

@socketio.on("hand")
def handle_hand(data): emit("hand", {"html": data["html"], "position": {"x": data["position"]["x"], "y": data["position"]["y"], "z": data["position"]["z"]}}, to = request.remote_addr, include_self = False)

@app.get("/robots.txt")
@app.get("/sitemap.xml")
@app.get("/manifest.json")
@app.get("/service-worker.js")
@app.get("/.well-known/assetlinks.json")
def serve_file(): return send_file(f"./{request.path}")

@app.errorhandler(404)
@app.errorhandler(405)
def error(_): return redirect("/")