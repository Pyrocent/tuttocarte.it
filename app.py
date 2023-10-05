from flask import (
    Flask,
    render_template
)

app = Flask(__name__)
app.template_folder = "templates/min"

app.route("/")
def index():
    return render_template("index.min.html")

if __name__ == "__main__": app.run(debug = True)