import functools
from flask import (
    Blueprint, flash, g, render_template, request, session, url_for
)

bp = Blueprint("auth", __name__, url_prefix="/auth")

@app.route("/")
def index():
    if "username" in session:
        return render_template("auth/index.html")

@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        session["username"] = request.form["username"]
        return redirect(url_for("index"))

@bp.route("/logout")
def logout():
    # remove the username from the session if it's there.
    session.pop("username", None)
    return redirect(url_for("index"))
