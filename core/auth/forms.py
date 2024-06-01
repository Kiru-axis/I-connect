from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from ..models import User
from wtforms import ValidationError


# Registration form
class RegistrationForm(FlaskForm):
    """
    class for registration of users
    """

    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=20)]
    )
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign up")

    def validate_email(self, data_field):
        if User.query.filter_by(email=data_field.data).first():
            raise ValidationError(message="The Email has already been taken!")

    def validate_username(self, data_field):
        if User.query.filter_by(username=data_field.data).first():
            raise ValidationError(message="The username has already been taken")


class LoginForm(FlaskForm):
    """
    class for login of users
    """

    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
        ],
    )
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")


class ForgotPasswordForm(FlaskForm):
    email = EmailField(label="Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Submit")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("Account not found. Please create one")


class ResetPasswordForm(FlaskForm):

    password = PasswordField(
        label="Password", validators=[DataRequired(), Length(min=3, max=15)]
    )
    confirm_password = PasswordField(
        label="Confirm Password",
        validators=[DataRequired(), EqualTo("password")],
    )
    submit = SubmitField("Reset")
