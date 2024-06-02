from os import listdir
from random import sample
from secrets import token_hex
from cryptography.fernet import Fernet
from flask_socketio import emit, SocketIO, join_room
from flask import Flask, request, redirect, send_file, render_template

fernet_object = Fernet(Fernet.generate_key())
encrypted_decks = {deck: [fernet_object.encrypt(card.encode()).decode().replace("==", "") for card in listdir(f"static/assets/decks/{deck}")] for deck in ["ita", "fr1", "fr2"]}

app = Flask(__name__)
socketio = SocketIO(app)
app.secret_key = token_hex(16)

@app.get("/")
def index(): return render_template("index.html", ita_deck = sample(encrypted_decks["ita"], 40), fr1_deck = sample(encrypted_decks["fr1"], 54), fr2_deck = sample(encrypted_decks["fr2"], 54))

@socketio.on("join")
def handle_join(data): join_room(data["room"]), emit("join", {"user": request.sid}, to = data["room"], include_self = False)

@socketio.on("play")
def handle_play(data): emit("play", {"html": data["html"]}, to = data["user"] if not data["room"] else data["room"], include_self = False)

@socketio.on("turn")
def handle_turn(data): emit("turn", {"id": data["id"], "value": fernet_object.decrypt(data["id"] + "==").decode()}, to = request.sid if not data["room"] else data["room"])

@socketio.on("hand")
def handle_hand(data): emit("hand", {"html": data["html"], "position": {"x": data["position"]["x"], "y": data["position"]["y"], "z": data["position"]["z"]}}, to = data["room"], include_self = False)

@app.get("/robots.txt")
@app.get("/sitemap.xml")
@app.get("/manifest.json")
@app.get("/service-worker.js")
@app.get("/.well-known/assetlinks.json")
def serve_file(): return send_file(f"./{request.path}")

@app.errorhandler(404)
@app.errorhandler(405)
def error(_): return redirect("/")