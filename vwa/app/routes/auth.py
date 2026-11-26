
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from app.forms import RegistrationForm, LoginForm
from app.services.auth_service import register_user, authenticate_user


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("auth.dashboard"))

    return redirect(url_for("auth.login"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user, error = register_user(
            form.username.data,
            form.email.data,
            form.password.data
        )

        if error:
            flash(error, "error")
        else:
            flash("Account created. You can now log in.", "success")
            return redirect(url_for("auth.login"))

    return render_template("register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = authenticate_user(
            form.username.data,
            form.password.data
        )

        if user is None:
            flash("Invalid username or password.", "error")
        else:
            login_user(user)

            flash("Logged in successfully.", "success")

            return redirect(url_for("auth.dashboard"))

    return render_template("login.html", form=form)


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()

    flash("You have been logged out.", "success")

    return redirect(url_for("auth.login"))


@auth_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template(
        "dashboard.html",
        user=current_user
    )
