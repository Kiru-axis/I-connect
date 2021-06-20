from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,Email,EqualTo
from ..models import User
from wtforms import ValidationError
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

    def validate_email(self,data_field):
        if User.query.filter_by(email = data_field.data).first():
            raise ValidationError(message="The Email has already been taken!")
    
    def validate_username(self, data_field):
        if User.query.filter_by(username = data_field.data).first():
            raise ValidationError(message="The username has already been taken")


class LoginForm(FlaskForm):
    """
    class for login of users
    """
    username = StringField('Username',validators=[DataRequired()])
    email = StringField("Email",validators=[DataRequired(),Email()])
    password = PasswordField("Password",validators=[DataRequired(),])
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")
