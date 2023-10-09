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
        rooms[room] = ["1B", "1C", "1D", "1S", "2B", "2C", "2D", "2S", "3B", "3C", "3D", "3S", "4B", "4C", "4D", "4S", "5B", "5C", "5D", "5S"]
        return render_template("index.min.html", room = room)
    elif room in list(rooms.keys()):
        return render_template("room.min.html", room = room)
    else:
        return redirect("/")

@socketio.on("join")
def join(data):
    join_room(data["room"])

@socketio.on("pick_from_deck")
def pick_from_deck(data):
    room = data["room"]
    deck = rooms[room]

    card = choice(deck)
    deck.remove(card)
    rooms[room] = deck

    if len(deck) == 0:
        emit("void", room = room)

    emit("pick", {"card": card}, room = data["user"])
    
@socketio.on("drop_from_deck")
def drop_from_deck(data):
    room = data["room"]
    deck = rooms[room]
    
    card = choice(deck)
    deck.remove(card)
    rooms[room] = deck

    if len(deck) == 0:
        emit("void", room = room)
        
    emit("drop", {"card": card}, room = room)

@socketio.on("drop_from_hand")
def drop_from_hand(data):
    emit("drop", {"card": data["card"]}, room = data["room"])
    
@socketio.on("pick_from_drop")
def pick_from_drop(data):
    card = data["card"]
    emit("pick", {"card": card}, room = data["user"])
    emit("pull", {"card": card}, room = data["room"])

@app.route("/robots")
def robots():
    return send_file("robots.txt")

@app.route("/sitemap")
def sitemap():
    return send_file("sitemap.txt")

if __name__ == "__main__": socketio.run(app, debug = True, allow_unsafe_werkzeug = True)