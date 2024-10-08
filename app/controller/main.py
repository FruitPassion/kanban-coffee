from flask import Blueprint, render_template
from flask_login import current_user, login_required

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("main/index.html")


@main.route("/profile")
@login_required
def profile():
    return render_template("main/profile.html", name=current_user.name)
