from flask import render_template, Blueprint, flash, request, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required

from flask import current_app

from core import db, bcrypt
from core.models import User
from core.auth.forms import (
    RegistrationForm,
    LoginForm,
    ResetPasswordForm,
    ForgotPasswordForm,
)


auth = Blueprint("auth", __name__)


# registration of users with
@auth.route("/register", methods=["POST", "GET"])
def register():
    # if the user is logged in, no need to go these page
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegistrationForm()

    if form.validate_on_submit():

        hashed_p = bcrypt.generate_password_hash(form.password.data).decode("utf-8")

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_p,
        )

        user.save()
        flash(f"Accout created for {user.username}", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


# login
@auth.route("/login", methods=["POST", "GET"])
def login():

    # if the user is logged in, no need to go these page
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            flash(f"Login success", "success")
            login_user(user, remember=form.remember.data)

            next_page = request.args.get("next")
            return (
                redirect(url_for(next_page))
                if next_page
                else redirect(url_for("main.index"))
            )
        else:
            flash("Invalid credentials", "error")

    return render_template("auth/login.html", form=form)


# logout
@auth.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("auth.login"))


@auth.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    # if the user is logged in, no need to go these page
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = ForgotPasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first_or_404()
        # send_reset_email(user)
        flash(
            "We have sent you a link to reset your password on the provided email",
            "info",
        )
        return redirect(url_for("auth.login"))

    return render_template("auth/forgot-password.html", form=form)


@auth.route("/reset-password/<string:token>", methods=["GET", "POST"])
def reset_password(token: str):

    # if the user is logged in, no need to go these page
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    user = User.verfy_reset_token(token=token)

    if user is None:
        flash("Invalid or Expired token", "warning")
        return redirect(url_for("auth.login"))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        hashed_p = bcrypt.generate_password_hash(form.password.data).decode("utf-8")

        user.password = hashed_p

        db.session.commit()

        flash(f"Password updated", "success")

        return redirect(url_for("auth.login"))

    return render_template("auth/reset-password.html", form=form)
