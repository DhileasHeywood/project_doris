import functools
from doris.models.entry_model import Entry
import json

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
bp = Blueprint("application", __name__, url_prefix="/application")


@bp.route("/", methods=["GET", "POST"])
def index():
    # I'm going to put this in the else statement afterwards, for if the request.method == "GET"


    # The start page needs to have the ability to start a new bid, and to search existing bids
    if request.method == "POST":
        if request.form["new_bid"]:
            return redirect(url_for("application.entry"))

        # elif button == "search":
            # search bids using some magical wizardry.
            # click on the bid title and make the bid object
            # session.bid = bid_title
            # return redirect(url_for("app.entry"))
    if "username" in session:
        return render_template("app/index.html")

    return redirect(url_for("auth.login"))


@bp.route("/entry", methods=["GET", "POST"])
def entry():
    # The entry page needs to have a search bar that can be used to find entries.
    # There need to be 4 boxes on the page. One for results, one for tags, one for project tags, and one for the body
    # There need to be buttons to update, add to a section, go to the section assembly, and add a new entry.
    if request.method == "POST":
        if request.form["go_to_section"]:
            return redirect(url_for("application.section"))

    return render_template("app/entry.html", current_bid = "Groovy Bid Title")

@bp.route("/entry_search", methods=["POST"])
def entry_search():
    # take the text from the search bar (and the checkboxes that I'll add.)
    # use it to form a query
    # Issue the query to the correct model (entry)
    # return a list of results.
    results = Entry.search(request.json)
    print(results.json())
    return json.dumps([(h['_source']) for h in results.json()['hits']['hits']])



@bp.route("/section", methods=["GET", "POST"])
def section():
    # The section page needs to have a section title and current bid line
    # There needs to be a box that displays the entries added to the current section
    # There need to be move up and move down buttons that will adjust the order of the sections in the box
    # On the right, there needs to be an editable text box that contains the text of the entries in the right order.
    # Underneath, there should be a save button and an add to bid button.
    if request.method == "POST":
        if request.form["go_to_bid"]:
            return redirect(url_for("application.bid"))

    return render_template("app/section.html")


@bp.route("/bid", methods=["GET", "POST"])
def bid():
    # The bid page needs to have the current bid title at the top
    # There needs to be a box for the sections, with move up and down buttons to control their order
    # There needs to be a text editor on the right with a save button that saves the bid.

    return render_template("app/bid.html")