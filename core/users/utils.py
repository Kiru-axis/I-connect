import secrets
import os
from flask_login import current_user
from PIL import Image

from flask import current_app


def save_image(form_picture):
    random_hex = secrets.token_hex(4)  # random_hex to distinguish images
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, "static/profiles/", picture_fn)
    # resizing
    output_size = (150, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    # print(current_user.image)
    os.remove(
        path=os.path.join(current_app.root_path, "static/profiles/", current_user.image)
    )
    i.save(picture_path)

    return picture_fn
