from random import choice
from uuid import uuid4
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

rooms = {}
app = Flask(__name__)
app.template_folder = "templates/min"
socketio = SocketIO(app)

@app.get("/")
@app.get("/<room>")
def index(room = None):
    if room == None:
        room = str(uuid4())
        rooms[room] = {
            "drop": [],
            "deck": ["1B", "1C", "1D", "1S", "2B", "2C", "2D", "2S", "3B", "3C", "3D", "3S", "4B", "4C", "4D", "4S", "5B", "5C", "5D", "5S"]
        }
        return render_template("index.min.html", room = room)
    elif room in list(rooms.keys()):
        return render_template("room.min.html", room = room)
    else:
        return redirect("/")

@socketio.on("join")
def join(data):
    room = data["room"]

    join_room(room)

    emit("drop", {"cards": rooms[room]["drop"]}, room = data["user"])

@socketio.on("pick_from_deck")
def pick_from_deck(data):
    room = data["room"]
    deck = rooms[room]["deck"]

    card = choice(deck)

    deck.remove(card)
    rooms[room]["deck"] = deck
    if len(deck) == 0:
        emit("void", room = room)

    emit("pick", {"card": card}, room = data["user"])

@socketio.on("drop_from_deck")
def drop_from_deck(data):
    room = data["room"]
    deck = rooms[room]["deck"]
    drop = rooms[room]["drop"]

    card = choice(deck)

    deck.remove(card)
    rooms[room]["deck"] = deck
    if len(deck) == 0:
        emit("void", room = room)

    drop.append(card)
    rooms[room]["drop"] = drop

    emit("drop", {"cards": rooms[room]["drop"]}, room = room)

@socketio.on("drop_from_hand")
def drop_from_hand(data):
    room = data["room"]
    drop = rooms[room]["drop"]

    drop.append(data["card"])
    rooms[room]["drop"] = drop

    emit("drop", {"cards": rooms[room]["drop"]}, room = room)

@socketio.on("pick_from_drop")
def pick_from_drop(data):
    room = data["room"]
    card = data["card"]
    drop = rooms[room]["drop"] 

    drop.remove(card)
    rooms[room]["drop"] = drop

    emit("pick", {"card": card}, room = data["user"])
    emit("drop", {"cards": rooms[room]["drop"]}, room = room)

@app.route("/robots")
def robots():
    return send_file("robots.txt")

@app.route("/sitemap")
def sitemap():
    return send_file("sitemap.txt")

if __name__ == "__main__": socketio.run(app, debug = True, allow_unsafe_werkzeug = True)