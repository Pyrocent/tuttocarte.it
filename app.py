from random import sample
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
    join_room,
    leave_room,
    room_exists
)

app = Flask(__name__)
app.template_folder = "templates/min"
socketio = SocketIO(app)

@app.get("/")
@app.get("/<id>")
def index(id = None):
    if id == None:
        id = uuid4()
        return render_template("index.min.html", room = id)
    elif room_exists(id):
        return render_template("room.min.html", room = id)
    else:
        return redirect("/")

@socketio.on("join_room")
def join_room(data):
    room = data["room"]
    user = data["user"]

    join_room(room)
    emit("join_room", ["1B", "1C", "1D", "1S"], room = user)

@socketio.on("leave_room")
def leave_room(data):
    room = data["room"]
    
    leave_room(room)

@socketio.on("draw_from_deck")
def draw_from_deck(data):
    room = data["room"]
    user = data["user"]
    deck = data["deck"]
    hand = data["hand"]
    draw = data["draw"]

    hand += sample(deck, draw)
    deck = [card for card in deck if card not in hand]

    emit("draw", hand, room = user)
    emit("deck", deck, room = room)

@socketio.on("drop_on_table")
def drop_on_table(data):
    room = data["room"]
    table = data["table"]
    cards = data["cards"]

    table += cards

    emit("table", table, room = room)

@app.route("/robots")
def robots():
    return send_file("robots.txt")

@app.route("/sitemap")
def sitemap():
    return send_file("sitemap.txt")

if __name__ == "__main__": socketio.run(app, debug = True, allow_unsafe_werkzeug = True)