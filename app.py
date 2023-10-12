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

# "deck": ["1B", "1C", "1D", "1S", "2B", "2C", "2D", "2S", "3B", "3C", "3D", "3S", "4B", "4C", "4D", "4S", "5B", "5C", "5D", "5S"]

# @socketio.on("join")
# def join(data):
#     room = data["room"]

#     join_room(room)

#     emit("drop", {"cards": rooms[room]["drop"]}, room = data["user"])
    
# @socketio.on("public_notes")
# def public_notes(data):
#     emit("public_notes", {"text": data["text"]}, room = data["room"])

# @socketio.on("deck_to_hand")
# def deck_to_hand(data):
#     room = data["room"]
#     deck = rooms[room]["deck"]

#     card = choice(deck)

#     deck.remove(card)
#     rooms[room]["deck"] = deck
#     if len(deck) == 0:
#         emit("void", room = room)

#     emit("pick", {"card": card}, room = data["user"])

# @socketio.on("deck_to_drop")
# def deck_to_drop(data):
#     room = data["room"]
#     deck = rooms[room]["deck"]
#     drop = rooms[room]["drop"]

#     card = choice(deck)

#     deck.remove(card)
#     rooms[room]["deck"] = deck
#     if len(deck) == 0:
#         emit("void", room = room)

#     drop.append(card)
#     rooms[room]["drop"] = drop

#     emit("drop", {"cards": rooms[room]["drop"]}, room = room)

# @socketio.on("hand_to_drop")
# def hand_to_drop(data):
#     room = data["room"]
#     drop = rooms[room]["drop"]

#     drop.append(data["card"])
#     rooms[room]["drop"] = drop

#     emit("drop", {"cards": rooms[room]["drop"]}, room = room)

# @socketio.on("drop_to_hand")
# def drop_to_hand(data):
#     room = data["room"]
#     card = data["card"]
#     drop = rooms[room]["drop"] 

#     drop.remove(card)
#     rooms[room]["drop"] = drop

#     emit("pick", {"card": card}, room = data["user"])
#     emit("drop", {"cards": rooms[room]["drop"]}, room = room)

app = Flask(__name__)
app.template_folder = "templates/min"
socketio = SocketIO(app)

@app.get("/")
@app.get("/<room>")
def index(room = None):
    if room == None:
        room = str(uuid4())
        return render_template("index.min.html", room = room, show = True)
    return render_template("index.min.html", room = room)

@app.route("/robots.txt")
def robots():
    return send_file("robots.txt")

@app.route("/sitemap.xml")
def sitemap():
    return send_file("sitemap.xml")

@app.route("/manifest.json")
def manifest():
    return send_file("manifest.json")

@app.route("/service-worker.js")
def service_worker():
    return send_file("service-worker.js")

@app.errorhandler(404)
@app.errorhandler(405)
def error(_):
    return redirect("/")

if __name__ == "__main__": socketio.run(app, debug = True, allow_unsafe_werkzeug = True)