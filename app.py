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
        rooms[room] = ["1B", "1C", "1D", "1S"]
        return render_template("index.min.html", room = room)
    elif room in list(rooms.keys()):
        return render_template("room.min.html", room = room)
    else:
        return redirect("/")

@socketio.on("join")
def join(data):
    join_room(data["room"])

@socketio.on("draw_from_deck")
def draw_from_deck(data):
    room = data["room"]
    deck = rooms[room]

    card = choice(deck)
    deck.remove(card)
    rooms[room] = deck

    if len(deck) == 0:
        emit("stop_deck", room = room)

    emit("draw", {"card": card}, room = data["user"])
    
@socketio.on("drop_from_deck")
def drop_from_deck(data):
    room = data["room"]
    deck = rooms[room]
    
    card = choice(deck)
    deck.remove(card)
    rooms[room] = deck

    if len(deck) == 0:
        emit("stop_deck", room = room)
        
    emit("drop", {"card": card}, room = room)

@app.route("/robots")
def robots():
    return send_file("robots.txt")

@app.route("/sitemap")
def sitemap():
    return send_file("sitemap.txt")

if __name__ == "__main__": socketio.run(app, debug = True, allow_unsafe_werkzeug = True)