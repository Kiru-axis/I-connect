from flask_wtf import FlaskForm
from wtforms import (
    SubmitField,
    EmailField,
)
from wtforms.validators import DataRequired, Email


# Subscribe form
class SubscriptionForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    subscribe = SubmitField("Subscribe")
