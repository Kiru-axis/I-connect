from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,Email,EqualTo
# Registration form
class RegistrationForm(FlaskForm):
    """
    class for registration of users
    """
    username = StringField("Username",validators=[DataRequired(),Length(min = 3,max =20)])
    email = StringField("Email",validators=[DataRequired(),Email()])
    password = PasswordField("Password",validators=[DataRequired(),])
    confirm_password = PasswordField("Password",validators=[DataRequired(),EqualTo("password")])
    submit = SubmitField("Sign up")

class LoginForm(FlaskForm):
    """
    class for login of users
    """
    email = StringField("Email",validators=[DataRequired(),Email()])
    password = PasswordField("Password",validators=[DataRequired(),])
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")
