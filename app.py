from flask import Flask, request, url_for, render_template, redirect
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    login_required,
    logout_user,
    current_user,
)
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from forms import *
from utils import *

app = Flask(__name__)
UPLOAD_FOLDER = "home/Documents/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
UPLOAD_FOLDER_ABS = os.path.join(app.root_path, "..", "..", UPLOAD_FOLDER)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER_ABS
app.config["SECRET_KEY"] = "secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    profile_image = db.Column(db.String(100), nullable=True)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(200))
    category = db.Column(db.String(50), nullable=False)
    image = db.Column(
        db.String(100), nullable=True
    )  # Assuming you'll store the image filename
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    author = db.relationship("User", backref=db.backref("articles", lazy=True))


@app.route("/")
def home():
    posts = Article.query.all()
    if current_user.is_authenticated:
        is_logged_in = True
    else:
        is_logged_in = False
    return render_template("main.html", is_logged_in=is_logged_in, posts=posts)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        profile_image = save_profile_image(form.profile_image.data)
        new_user = User(
            name=form.name.data,
            email=form.email.data,
            password=hashed_password,
            profile_image=profile_image,
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("dashboard"))
    return render_template("login.html", form=form)


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    user = User.query.get(current_user.id)
    form = ArticleForm()
    if form.validate_on_submit():
        image_filename = save_article_image(form.image.data)
        new_article = Article(
            title=form.title.data,
            subtitle=form.subtitle.data,
            category=form.category.data,
            image=image_filename,
            content=form.content.data,
            author_id=current_user.id,
            author=current_user,
        )
        db.session.add(new_article)
        db.session.commit()
        return redirect(url_for("dashboard"))
    return render_template("dashboard.html", user=user, form=form)


@app.route("/post/<int:post_id>")
def post(post_id):
    if current_user.is_authenticated:
        is_logged_in = True
    else:
        is_logged_in = False
    article = Article.query.get_or_404(post_id)
    return render_template("post-page.html", article=article, is_logged_in=is_logged_in)


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
