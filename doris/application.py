import functools
from doris.models.entry_model import Entry
import json
from datetime import date

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
    print("entry page")

    return render_template("app/entry.html", current_bid = "Groovy Bid Title")

@bp.route("/entry_search", methods=["POST"])
def entry_search():
    # take the text from the search bar (and the checkboxes that I'll add.)
    # use it to form a query
    # Issue the query to the correct model (entry)
    # return a list of results.

    results = Entry.search(request.json)

    return json.dumps([[h['_source'], h['_id']] for h in results.json()['hits']['hits']])

@bp.route("/entry_update", methods=["POST"])
def entry_update():
    # take the information from the tags, project tags and body tags, and update the entry with those details.

    update_data = request.json

    new_tags = update_data["tags_new"]
    new_project_tags = update_data["project_tags_new"]
    new_body = update_data["body_new"]
    update_id = update_data["entry_id"]

    retrieved_doc = Entry.retrieve(update_id)

    doc_id = retrieved_doc.json()["_id"]
    tags = retrieved_doc.json()["_source"]["tags"]
    project_tags = retrieved_doc.json()["_source"]["project_tags"]
    body = retrieved_doc.json()["_source"]["body"]
    user = retrieved_doc.json()["_source"]["user"]
    update_date = str(date.today())
    version = retrieved_doc.json()["_source"]["version"] + 1

    update_doc = Entry(tags=tags, project_tags=project_tags, body=body, user=user, date=update_date,
                                   version=version, id=doc_id)

    update = update_doc.update(new_project_tags=new_project_tags, new_tags=new_tags, new_body=new_body)

    print(update)

    return json.dumps(update.status_code)



@bp.route("/section", methods=["GET", "POST"])
def section():
    """ The section page needs to have a section title and current bid line
    There needs to be a box that displays the entries added to the current section
    There need to be move up and move down buttons that will adjust the order of the sections in the box
    On the right, there needs to be an editable text box that contains the text of the entries in the right order.
    Underneath, there should be a save button and an add to bid button."""
    if request.method == "POST":
        if request.form["go_to_bid"]:
            return redirect(url_for("application.bid"))
        elif request.form["change_bid"]:
            return redirect(url_for("application.index"))

    return render_template("app/section.html")


@bp.route("/bid", methods=["GET", "POST"])
def bid():
    # The bid page needs to have the current bid title at the top
    # There needs to be a box for the sections, with move up and down buttons to control their order
    # There needs to be a text editor on the right with a save button that saves the bid.
    # if request.method == "POST":
    #    if request.form["change_bid"]:

    return render_template("app/bid.html")