from flask import (
    Flask,
    send_file,
    render_template
)

rooms = {}

app = Flask(__name__)
app.template_folder = "templates/min"

@app.get("/")
def index():
    return render_template("index.min.html")

@app.route("/robots")
def robots():
    return send_file("robots.txt")

@app.route("/sitemap")
def sitemap():
    return send_file("sitemap.txt")

if __name__ == "__main__": app.run(debug = True)