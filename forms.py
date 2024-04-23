from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    name = StringField(
        "name",
        validators=[DataRequired(), Length(min=2, max=20)],
        render_kw={"placeholder": "Name"},
    )
    email = StringField(
        "email",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Email"},
    )
    password = PasswordField(
        "pwd", validators=[DataRequired()], render_kw={"placeholder": "Password"}
    )
    confirm_password = PasswordField(
        "cnfPwd",
        validators=[DataRequired(), EqualTo("password")],
        render_kw={"placeholder": "Confirm Password"},
    )
    profile_image = FileField(
        "Profile Image", validators=[FileRequired(), FileAllowed(["jpg", "png"])]
    )
    submit = SubmitField("Signup")


class LoginForm(FlaskForm):
    email = StringField(
        "email",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Email"},
    )
    password = PasswordField(
        "pwd", validators=[DataRequired()], render_kw={"placeholder": "Password"}
    )
    submit = SubmitField("Login")


class ArticleForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=100)])
    subtitle = StringField("Subtitle", validators=[Length(max=200)])
    category = StringField("Category", validators=[DataRequired(), Length(max=50)])
    image = FileField("Image", validators=[FileAllowed(["jpg", "png", "jpeg"])])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Create article")
