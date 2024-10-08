from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from model.shared_model import User, db
from utils import app_security

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/login")
def login():
    return render_template("auth/login.html")


@auth.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(email=email).first()

    if not user or not app_security.compare_passwords(password, user.password):
        flash("Please check your login details and try again.")
        return redirect(url_for("auth.login"))

    login_user(user, remember=remember)
    return redirect(url_for("main.profile"))


@auth.route("/register")
def register():
    return render_template("auth/register.html")


@auth.route("/register", methods=["POST"])
def register_post():
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")

    user = User.query.filter_by(email=email).first()
    if user:
        flash("Email address already exists")
        return redirect(url_for("auth.redirect"))

    new_user = User(
        email=email,
        username=username,
        password=app_security.encrypt_password(password),
        lastname=lastname,
        firstname=firstname,
    )

    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for("auth.login"))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
