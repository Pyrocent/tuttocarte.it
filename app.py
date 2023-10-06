from flask import (
    Flask,
    send_file,
    render_template
)
from flask_socketio import (
    emit,
    SocketIO,
    join_room,
    leave_room
)

rooms = {}
IDs = set()

app = Flask(__name__)
app.template_folder = "templates/min"
socketio = SocketIO(app)

@app.get("/")
def index():
    return render_template("index.min.html")

@app.post("/")
def get_id():
    socketio.emit("join", id)
    return render_template("room.min.html")

@socketio.on("join")
def join(data):
    print(data)
    room_id = data["room_id"]
    username = data["username"]
    join_room(room_id)
    if room_id not in rooms:
        rooms[room_id] = []
    rooms[room_id].append(username)
    emit('update_players', rooms[room_id], room=room_id)
    emit('message', f'{username} è entrato nella room.', room=room_id)

@socketio.on('leave')
def leave(data):
    room_id = data['room_id']
    username = data['username']
    leave_room(room_id)
    if room_id in rooms:
        rooms[room_id].remove(username)
        emit('update_players', rooms[room_id], room=room_id)
        emit('message', f'{username} ha lasciato la room.', room=room_id)

@socketio.on('chat_message')
def chat_message(data):
    room_id = data['room_id']
    username = data['username']
    message = data['message']
    emit('chat_message', {'username': username, 'message': message}, room=room_id)

@app.route("/robots")
def robots():
    return send_file("robots.txt")

@app.route("/sitemap")
def sitemap():
    return send_file("sitemap.txt")

if __name__ == "__main__": socketio.run(app, debug = True, allow_unsafe_werkzeug = True)