from flask import (
    redirect,
    request,
    flash,
    render_template,
    url_for,
    Blueprint,
)

from core import db

from flask_login import current_user, login_required

from core.models import Blog, User


main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
def index():

    # INSTEAD OF PAGINATION, CAN BE IMPROVED WITH INFINITE SCROLL
    blog_page = request.args.get("blog_page", 1, type=int)
    user_page = request.args.get("user_page", 1, type=int)

    blogs = Blog.query.order_by(Blog.date_posted.desc()).paginate(
        per_page=10, page=blog_page
    )

    users = User.query.paginate(per_page=10, page=user_page)
    return render_template("index.html", blogs=blogs, users=users)


# THE BELOW METHODS ARE SIMILAR TO THE ONES IN PROFILE WITH THE CHANGES BEING THE ROUTES
# BOTH CAN BE IMPROVED WITH JAVASCRIPT


# follow
@main.route("/follow_home/<string:username>", methods=["GET", "POST"])
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()

    if user is None:
        flash("User not found", "error")
        return redirect(url_for("main.index", username=username))

    if user == current_user:
        flash("You cannot follow yourself", "error")
        return redirect(url_for("main.index", username=username))

    new_follower = current_user.follow(user)
    if new_follower is None:
        flash(f"You are already following {user.username}", "info")
        return redirect(url_for("main.index", username=username))
    db.session.add(new_follower)
    db.session.commit()
    flash(f"You are now following {user.username}", "success")

    return redirect(url_for("main.index", username=username))


# unfollow
@main.route("/unfollow_home/<string:username>", methods=["GET", "POST"])
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()

    if user is None:
        flash("User not found", "error")
        return redirect(url_for("main.index", username=username))

    if user == current_user:
        flash("You cannot unfollow yourself", "error")
        return redirect(url_for("main.index", username=username))

    new_follower = current_user.unfollow(user)
    if new_follower is None:
        flash(f"You have already unfollowed {user.username}", "info")
        return redirect(url_for("main.index", username=username))
    db.session.add(new_follower)
    db.session.commit()
    flash(f"You have unfollowed {user.username}", "success")

    return redirect(url_for("main.index", username=username))
