from flask import Flask, request, url_for, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("main.html")

@app.route("/blogpost")
def blog():
    return render_template("post-page.html")
if __name__ == "__main__":
    app.run(debug=True)
