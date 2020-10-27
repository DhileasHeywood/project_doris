import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
bp = Blueprint("application", __name__, url_prefix="/application")


@bp.route("/", methods=["GET", "POST"])
def index():
    # I'm going to put this in the else statement afterwards, for if the request.method == "GET"
    if "username" in session:
        return render_template("app/index.html")

    # The start page needs to have the ability to start a new bid, and to search existing bids
    # if request.method == "POST":
        # if button == "new bid":
            # return redirect(url_for("app.entry"))

        # elif button == "search":
            # search bids using some magical wizardry.
            # click on the bid title and make the bid object
            # session.bid = bid_title
            # return redirect(url_for("app.entry"))

    return redirect(url_for("auth.login"))


@bp.route("/entry")
def entry():
    # The entry page needs to have a search bar that can be used to find entries.
    # There need to be 4 boxes on the page. One for results, one for tags, one for project tags, and one for the body
    # There need to be buttons to update, add to a section, go to the section assembly, and add a new entry.


    pass