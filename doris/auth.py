import functools
from flask import (
    Blueprint, flash, g, render_template, request, session, url_for
)

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        error = none

        if not username:
            error = "A name is required."
