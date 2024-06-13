from os import listdir
from random import choice
from secrets import token_hex
from flask_socketio import emit, SocketIO, join_room
from flask import Flask, request, redirect, send_file, render_template

decks = {
    "it": listdir("static/assets/decks/it"),
    "fr": listdir("static/assets/decks/fr")
}

socketio = SocketIO(app := Flask(__name__))
app.secret_key = token_hex(16)

@app.get("/")
def index(): return render_template("index.html")

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
def handle_play(data): emit("play", {"html": data["html"]}, to = data["user"])

@socketio.on("show")
def handle_show(data): emit("show", {"card": data["card"], "deck": data["deck"], "exit": data["exit"] if not isinstance(data["exit"], list) else choice([i for i in decks[data["deck"]] if i not in data["exit"]])}, to = data["room"])

@socketio.on("hide")
def handle_hide(data): emit("hide", {"card": data["card"], "deck": data["deck"]}, to = data["room"])

@socketio.on("hand")
def handle_hand(data): emit("hand", {"html": data["html"], "x": data["x"], "y": data["y"], "z": data["z"]}, to = data["room"], include_self = False)