import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint("app", __name__, url_prefix="/app")


@bp.route("/")
def index():
    if "username" in session:
        return render_template("app/index.html")

    return redirect(url_for("auth.login"))


@bp.route("/start", methods=("GET", "POST"))
def start():
    # The start page needs to have the ability to start a new bid, and to search existing bids
    # if request.method == "POST":
        # if button == "new bid":
            # return redirect(url_for("app.entry"))+
    # elif request.method == "GET":
        # if button == "search":
            # search bids using some magical wizardry.
            # click on the bid title and make the bid object
            # session.bid = bid_title
            # return redirect(url_for("app.entry"))

    pass

@bp.route("/entry")
def entry():
    # The entry page needs to have a search bar that can be used to find entries.
    # There need to be 4 boxes on the page. One for results, one for tags, one for project tags, and one for the body
    # There need to be buttons to update, add to a section, go to the section assembly, and add a new entry.


    pass