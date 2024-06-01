from flask_wtf import FlaskForm
from wtforms import SubmitField, ValidationError, TextAreaField, StringField, EmailField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.file import FileAllowed, FileSize, FileField
from flask_login import current_user

from core.models import User


class UpdateProfileForm(FlaskForm):
    username = StringField(
        label="Username", validators=[DataRequired(), Length(min=2, max=30)]
    )
    email = EmailField(label="Email", validators=[DataRequired(), Email()])

    bio = TextAreaField("Tell us about you.", validators=[DataRequired()])

    image = FileField(
        label="Image",
        validators=[
            FileAllowed(
                ["png", "jpg"], FileSize(2 * 1024 * 1024, 0, "size limit exceeded")
            )
        ],
    )

    submit = SubmitField("Update")

    # class validators
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        if username.data != current_user.username:
            if user:
                raise ValidationError(
                    "Username already exists. Please select another one"
                )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if email.data != current_user.email:
            if user:
                raise ValidationError("Email already exists. Please select another one")
