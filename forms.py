from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
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
