from os import listdir
from random import sample
from secrets import token_hex
from flask_socketio import emit, SocketIO, join_room
from flask import Flask, request, redirect, send_file, render_template

app = Flask(__name__)
socketio = SocketIO(app)
app.secret_key = token_hex(16)

@app.get("/")
def index(): return render_template("index.html", ita_deck = sample(listdir(f"static/assets/decks/ita"), 40), fr1_deck = sample(listdir(f"static/assets/decks/fra"), 54), fr2_deck = sample(listdir(f"static/assets/decks/fra"), 54))

@app.get("/robots.txt")
@app.get("/sitemap.xml")
@app.get("/manifest.json")
@app.get("/service-worker.js")
@app.get("/.well-known/assetlinks.json")
def serve_file(): return send_file(f"./{request.path}")

@app.errorhandler(404)
@app.errorhandler(405)
def error(_): return redirect("/")

@socketio.on("join")
def handle_join(data): join_room(data["room"]), emit("join", {"user": request.sid}, to = data["room"], include_self = False)

@socketio.on("play")
def handle_play(data): emit("play", {"html": data["html"]}, to = data["user"] if not data["room"] else data["room"], include_self = False)

@socketio.on("hand")
def handle_hand(data): emit("hand", {"html": data["html"], "position": {"x": data["position"]["x"], "y": data["position"]["y"], "z": data["position"]["z"]}}, to = data["room"], include_self = False)

socketio.run(app, debug = True)