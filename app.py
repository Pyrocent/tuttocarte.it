from cryptography.fernet import Fernet
from secrets import token_hex
from random import shuffle
from time import time
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

encryption_key = Fernet.generate_key()
encrypted_italian_deck = [Fernet(encryption_key).encrypt(card.encode()).decode() for card in ["1B", "1C", "1D", "1S", "2B", "2C", "2D", "2S", "3B", "3C", "3D", "3S", "4B", "4C", "4D", "4S", "5B", "5C", "5D", "5S", "6B", "6C", "6D", "6S", "7B", "7C", "7D", "7S", "8B", "8C", "8D", "8S", "9B", "9C", "9D", "9S", "10B", "10C", "10D", "10S"]]
encrypted_french1_deck = [Fernet(encryption_key).encrypt(card.encode()).decode() for card in ["1C", "1F", "1P", "1Q", "2C", "2F", "2P", "2Q", "3C", "3F", "3P", "3Q", "4C", "4F", "4P", "4Q", "5C", "5F", "5P", "5Q", "6C", "6F", "6P", "6Q", "7C", "7F", "7P", "7Q", "8C", "8F", "8P", "8Q", "9C", "9F", "9P", "9Q", "10C", "10F", "10P", "10Q", "JC", "JF", "JP", "JQ", "QC", "QF", "QP", "QQ", "KC", "KF", "KP", "KQ", "BJ", "RJ"]]
encrypted_french2_deck = [Fernet(encryption_key).encrypt(card.encode()).decode() for card in ["1C", "1F", "1P", "1Q", "2C", "2F", "2P", "2Q", "3C", "3F", "3P", "3Q", "4C", "4F", "4P", "4Q", "5C", "5F", "5P", "5Q", "6C", "6F", "6P", "6Q", "7C", "7F", "7P", "7Q", "8C", "8F", "8P", "8Q", "9C", "9F", "9P", "9Q", "10C", "10F", "10P", "10Q", "JC", "JF", "JP", "JQ", "QC", "QF", "QP", "QQ", "KC", "KF", "KP", "KQ", "BJ", "RJ"]]

app = Flask(__name__)
app.secret_key = token_hex(16)
app.template_folder = "templates/min"
socket = SocketIO(app)

@app.get("/")
@app.get("/<room>")
def index(room = None):
    if room is not None:
        return render_template("index.min.html", room = room)

    shuffle(encrypted_italian_deck)
    shuffle(encrypted_french1_deck)
    shuffle(encrypted_french2_deck)

    return render_template(
        "index.min.html",
        room = int(time()),
        dealer = True,
        html = f"""
            <div class = "deck">
                {"".join([f'<img id = "{card}" class = "italian card" src = "static/assets/decks/italian/BACK.jpg" alt = "card">' for card in encrypted_italian_deck])}
            </div>
            <div class = "deck">
                {"".join([f'<img id = "{card}" class = "french1 card" src = "static/assets/decks/french1/BACK.jpg" alt = "card">' for card in encrypted_french1_deck])}
            </div>
            <div class = "deck">
                {"".join([f'<img id = "{card}" class = "french2 card" src = "static/assets/decks/french2/BACK.jpg" alt = "card">' for card in encrypted_french2_deck])}
            </div>
            <img id = "fiche1" class = "fiche" src = "static/assets/fiches/FICHE1.png" alt = "fiche">
            <img id = "fiche2" class = "fiche" src = "static/assets/fiches/FICHE2.png" alt = "fiche">
            <img id = "fiche3" class = "fiche" src = "static/assets/fiches/FICHE3.png" alt = "fiche">
            <img id = "dealer" class = "fiche" src = "static/assets/fiches/DEALER.png" alt = "fiche">
        """)

@socket.on("join")
def join(data):
    join_room(data["room"])

@socket.on("draw")
def draw(data):
    emit("draw", {"card": Fernet(encryption_key).decrypt(data["id"]).decode()}, room = data["room"])

@socket.on("table")
def table(data):
    emit("table", {"html": data["html"]}, room = data["room"])

@socket.on("notes")
def notes(data):
    emit("notes", {"notes": data["notes"]}, room = data["room"])

@app.route("/robots.txt")
def robots():
    return send_file("robots.txt")

@app.route("/sitemap.xml")
def sitemap():
    return send_file("sitemap.xml")

@app.route("/app.webmanifest")
def manifest():
    return send_file("app.webmanifest")

@app.route("/service-worker.js")
def service_worker():
    return send_file("service-worker.js")

@app.errorhandler(404)
@app.errorhandler(405)
def error(_):
    return redirect("/")

if __name__ == "__main__": socket.run(app,allow_unsafe_werkzeug=True)