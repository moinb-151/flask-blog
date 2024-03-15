from flask import Flask, request, url_for, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("main.html")

@app.route("/blogpost")
def blog():
    return render_template("post-page.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/login")
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
