from os import listdir
from random import sample
from secrets import token_hex
from flask import Flask, request, redirect, send_file, render_template

app = Flask(__name__, template_folder = "app/templates", static_folder = "app/static")
app.secret_key = token_hex(16)

@app.before_request
def redirect_www():
    if request.host.startswith("www"): return redirect(request.url.replace("www.", "")), 301

@app.get("/")
def index():
    return render_template(
        "min/index.min.html",
        ita_deck = sample(listdir("./src/app/static/assets/decks/ita"), 40),
        blue_fra_deck = sample(listdir("./src/app/static/assets/decks/fra/"), 52),
        red_fra_deck = sample(listdir("./src/app/static/assets/decks/fra/"), 52)
    ), 200

@app.get("/robots.txt")
@app.get("/sitemap.xml")
@app.get("/manifest.json")
@app.get("/service-worker.js")
@app.get("/.well-known/assetlinks.json")
def serve_file(): return send_file(f"app/{request.path}"), 200

@app.errorhandler(404)
def page_not_found(_): return render_template("/errors/min/404.min.html"), 404

@app.errorhandler(405)
def method_not_allowed(_): return render_template("/errors/min/405.min.html"), 405

if __name__ == "__main__": app.run(debug = True)