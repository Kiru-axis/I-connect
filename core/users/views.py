from flask import (
    redirect,
    request,
    flash,
    render_template,
    abort,
    url_for,
    Blueprint,
)
from flask_login import current_user, login_required
from core import db
from core.models import User, Blog
from core.users.forms import UpdateProfileForm
from core.users.utils import save_image

users = Blueprint("users", __name__)


@users.route("/user/<username>")
def profile(username):
    user = User.query.filter_by(username=username).first()
    blogs = Blog.query.filter_by(user=user).all()

    if user is None:
        flash("User not found", "error")
        return redirect(url_for("main.index"))

    user_image = None

    if current_user.is_authenticated:
        user_image = url_for("static", filename="profiles/" + current_user.image)
    else:
        user_image = url_for("static", filename="profiles/avatar.png")

    return render_template(
        "profile/profile.html",
        user=user,
        user_image=user_image,
        blogs=blogs,
        followers=user.followers.count(),
        followed=user.followed.count(),
    )


# follow
@users.route("/user/follow/<string:username>", methods=["GET", "POST"])
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()

    if user is None:
        flash("User not found", "error")
        return redirect(url_for("users.profile", username=username))

    if user == current_user:
        flash("You cannot follow yourself", "error")
        return redirect(url_for("users.profile", username=username))

    new_follower = current_user.follow(user)
    if new_follower is None:
        flash(f"You are already following {user.username}", "info")
        return redirect(url_for("users.profile", username=username))
    db.session.add(new_follower)
    db.session.commit()
    flash(f"You are now following {user.username}", "success")

    return redirect(url_for("users.profile", username=username))


# unfollow
@users.route("/user/unfollow/<string:username>", methods=["GET", "POST"])
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()

    if user is None:
        flash("User not found", "error")
        return redirect(url_for("users.profile", username=username))

    if user == current_user:
        flash("You cannot unfollow yourself", "error")
        return redirect(url_for("users.profile", username=username))

    new_follower = current_user.unfollow(user)
    if new_follower is None:
        flash(f"You have already unfollowed {user.username}", "info")
        return redirect(url_for("users.profile", username=username))
    db.session.add(new_follower)
    db.session.commit()
    flash(f"You have unfollowed {user.username}", "success")

    return redirect(url_for("users.profile", username=username))


# update profile
@users.route("/user/<username>/update", methods=["GET", "POST"])
@login_required
def update_profile(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)

    form = UpdateProfileForm()
    print(form.data)

    if form.validate_on_submit():
        if form.image.data:
            image_file = save_image(form.image.data)
            user.image = image_file
        # update the current user directly
        user.username = form.username.data
        user.email = form.email.data
        user.bio = form.bio.data
        db.session.commit()
        flash("Account updated", "success")
        return redirect(url_for("users.profile", username=user.username))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio
    return render_template("profile/update.html", form=form)
