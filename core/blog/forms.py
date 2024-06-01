from flask_wtf import FlaskForm
from wtforms import (
    SubmitField,
    TextAreaField,
    FileField,
)
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed, FileSize, FileField


# giving the user abilty to create posts
class CreateBlogForm(FlaskForm):
    content = TextAreaField("Content", validators=[DataRequired()])
    image = FileField(
        label="Image",
        validators=[
            DataRequired(),
            FileAllowed(
                ["png", "jpg"], FileSize(2 * 1024 * 1024, 0, "size limit exceeded")
            ),
        ],
    )
    submit = SubmitField("Post")
