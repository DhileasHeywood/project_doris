import functools
from doris.models.entry_model import Entry
from doris.models.bid_model import Bid
from doris.models.section_model import Section
import json
from datetime import date
from uuid import uuid4
from markdownify import markdownify as md
from datetime import date

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
bp = Blueprint("application", __name__, url_prefix="/application")


@bp.route("/", methods=["GET", "POST"])
def index():
    #Retrieving the bid titles to use in search box.
    resp = Bid.search()

    if resp.status_code != 200:
        print("You have no data!")
        session["extant_bids"] = []
    else:
        results = resp.json()
        bid_search = [
            {"id": h["_id"], "title": h["_source"]["title"]}
            for h in results.get("hits", {}).get("hits")
        ]
        bids = {
            h["_id"]: h["_source"]["title"]
            for h in results["hits"]["hits"]
        }
        session["extant_bids"] = bid_search

    # The start page needs to have the ability to start a new bid, and to search existing bids
    if request.method == "POST":

        if request.form.get("bid_search", None):

            current_bid = bids[request.form["bid_search"]]
            bid_id = request.form["bid_search"]

            return redirect(url_for("application.entry", bid_id=bid_id, current_bid=current_bid))


        if request.form.get("new_bid_title", None):

            extant_bids = []
            for bid in bid_search:
                extant_bids.append(bid["title"])

            if request.form["new_bid_title"] not in extant_bids:

                current_bid = request.form["new_bid_title"]
                new_id = str(uuid4())
                new_bid = Bid(title=current_bid, user=session["username"], date=str(date.today()), version=0, body="None",
                              sections=["None"], new_id=new_id)


                new_bid.create()

                return redirect(url_for("application.entry", current_bid=current_bid, bid_id=new_id))

            else:
                print("this bid already exists!")

            # provide some sort of verification. You shouldn't be able to create duplicates of bids.
            # retrieve the id of the new bid and assign it to bid_id.



    if "username" in session:
        return render_template("app/index.html")

    return redirect(url_for("auth.login"))


@bp.route("/entry/<current_bid>/<bid_id>", methods=["GET", "POST"])
def entry(bid_id=None, current_bid=None):

    section_results = Section.search().json()
    section_search = [{"id": h["_id"], "title" : h["_source"]["title"], "project_tags": h["_source"]["project_tags"]}
        for h in section_results["hits"]["hits"]]
    session.extant_sections = section_search
    # create a list of section titles to be searched, and compared to prevent duplicate names
    section_titles = []
    for sect in section_search:
        section_titles.append(sect["title"])


    if request.method == "POST":
        # Either the section will already exist, and will have a bid or bids associated with it
        # or the section will not exist and can be created.

        # If the New Section button is pressed, the title of the section should be checked against
        # existing section titles
        new_title = request.form.get("new_section_title")
        if new_title:
            if new_title not in section_titles:
            # if section title already exists, then don't allow
                new_id = str(uuid4())
                new_section = Section(title=new_title, tags=None, project_tags=current_bid, user=session["username"],
                                      version=0, body=None, entries=None, date=str(date.today()), new_id=new_id)
                new_section.create()

            else:
                print("This section already exists!")


        elif request.form.get("search_extant_sections"):
            pass

        # If the Search Existing Sections button is pressed, then there should be a search bar
        # similar to that of the search for existing bids search in index.


    # basic view function for entry page. Passes in params for current bid and bid id so that page can be accessed.
    return render_template("app/entry.html", current_bid=current_bid, bid_id=bid_id)


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
    update_data = request.json

    update_data["new_body"] = md(update_data["new_body"], heading_style="ATX")

    update_id = update_data["entry_id"]

    # retrieve ES document with matching ID and make it an Entry object
    retrieved_doc = Entry.retrieve(update_id)

    # update the Entry object with the data from the front end
    # The **update_data unpacks the keyword arguments into the right places automatically.
    update = retrieved_doc.update(**update_data)

    # sends the status code to front end to tell it if the update was successful
    return json.dumps(update.status_code)

@bp.route("/section_search", methods=["POST"])
def section_search():
#   take the result from the select box
#   use it to retrieve a dictionary entry
#   return the dictionary entry for use by the front end

    section_results = Section.search().json()

    section_search_by_id = {
        h["_id"]: {
            "id": h["_id"],
            "title": h["_source"]["title"],
            "project_tags": h["_source"]["project_tags"]}
        for h in section_results["hits"]["hits"]
    }
    id = section_search_by_id[request.json]

    return json.dumps(id)

@bp.route("/section/<current_bid>/<bid_id>", methods=["GET", "POST"])
def section(bid_id=None, current_bid=None):
    """ The section page needs to have a section title and current bid line
    There needs to be a box that displays the entries added to the current section
    There need to be move up and move down buttons that will adjust the order of the sections in the box
    On the right, there needs to be an editable text box that contains the text of the entries in the right order.
    Underneath, there should be a save button and an add to bid button."""
    if request.method == "POST":
        if request.form["go_to_bid"]:
            return redirect(url_for("application.bid", current_bid=current_bid, bid_id=bid_id))
        elif request.form["change_bid"]:
            return redirect(url_for("application.index", current_bid=current_bid, bid_id=bid_id))

    return render_template("app/section.html", current_bid=current_bid, bid_id=bid_id)


@bp.route("/bid/<current_bid>/<bid_id>", methods=["GET", "POST"])
def bid(bid_id=None, current_bid=None):
    # The bid page needs to have the current bid title at the top
    # There needs to be a box for the sections, with move up and down buttons to control their order
    # There needs to be a text editor on the right with a save button that saves the bid.
    # if request.method == "POST":
    #    if request.form["change_bid"]:

    return render_template("app/bid.html", current_bid=current_bid, bid_id=bid_id)
