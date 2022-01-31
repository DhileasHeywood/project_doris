import requests
import json
import time

# The basic class of an elasticsearch object.
# This will be the parent class for entries, sections and bids, as well as images

#ELASTICSEARCH_URL = "http://localhost:9200/doris-"
ELASTICSEARCH_URL = "http://doris_es:9200/doris-"

# fixme: we could import the ElasticsearchObject and models below from doris rather than duplicating it here
class ElasticsearchObject(object):
    def __init__(self, **kwargs):
        pass

    es_type = None
    data = None

    def create(self):
        # build the url
        url = ELASTICSEARCH_URL + self.es_type + "/_doc"

        # create the payload - transform self.data to JSON
        payload = json.dumps(self.data)
        print(payload)
        headers = {
            'Content-Type': 'application/json'
        }

        # Send the request to elasticsearch
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response)

        return response


class EntryObject(ElasticsearchObject):
    es_type = "entry"

    def __init__(self, **kwargs):
        super(EntryObject, self).__init__(**kwargs)
        if self.data is None:
            self.data = {}
        self.data["tags"] = kwargs["tags"]
        self.data["project_tags"] = kwargs["project_tags"]
        self.data["body"] = kwargs["body"]
        self.data["user"] = kwargs["user"]
        self.data["date"] = kwargs["date"]
        self.data["version"] = kwargs["version"]
        if kwargs.get("id"):
            self.data["id"] = kwargs["id"]


class SectionObject(ElasticsearchObject):
    es_type = "section"

    def __init__(self, **kwargs):
        super(SectionObject, self).__init__(**kwargs)
        if self.data is None:
            self.data = {}
        self.data["title"] = kwargs["title"]
        self.data["tags"] = kwargs["tags"]
        self.data["project_tags"] = kwargs["project_tags"]
        self.data["body"] = kwargs["body"]
        self.data["entries"] = kwargs["entries"]
        self.data["user"] = kwargs["user"]
        self.data["date"] = kwargs["date"]
        self.data["version"] = kwargs["version"]


class BidObject(ElasticsearchObject):
    es_type = "bid"

    def __init__(self, **kwargs):
        super(BidObject, self).__init__(**kwargs)
        if self.data is None:
            self.data = {}
        self.data["title"] = kwargs["title"]
        self.data["body"] = kwargs["body"]
        self.data["sections"] = kwargs["sections"]
        self.data["user"] = kwargs["user"]
        self.data["date"] = kwargs["date"]
        self.data["version"] = kwargs["version"]


# To assemble a query. The search function requires a query as an argument.
def make_query(search_type, search_text):
    if search_type == "body":
        query_object = {
            "query": {
                "match": {
                    "body": {
                        "query": search_text
                    }
                }
            },
            "size": 1}

        return query_object


# To search for an entry. Because it's not part of a class, you have to enter an es_type argument. can't figure out how
# to make it part of a class because these don't exist yet.
def search(query=None, es_type=None):
    if query is None:
        query = {
            "query": {
                "match_all": {}}}


    if es_type is not None:
        url = ELASTICSEARCH_URL + es_type + "/_search"
    else:
        raise Exception("Please put in an es_type. Geez Dhileas.")

    payload = json.dumps(query)
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response


# To get the id of an entry or section to be able to add it to a section or bid
def get_id(query_text):

    return query_text.json()['hits']['hits'][0]['_id']

    #return json.dumps(results.json()['hits']['hits']['_id'])


entry_1 = EntryObject(tags=["test", "fake", "joke", "practice"], project_tags=["doris", "geraldine"],
                      body=" A manager, a mechanical engineer, and software analyst are driving back from convention "
                           "through the mountains. Suddenly, as they crest a hill, the brakes on the car go out and "
                           "they fly careening down the mountain. After scraping against numerous guardrails, they come"
                           " to a stop in the ditch. Everyone gets out of the car to assess the damage. The manager "
                           "says, 'Let's form a group to collaborate ideas on how we can solve this issue.' The "
                           "mechanical engineer suggests, 'We should disassemble the car and analyze each part for "
                           "failure.' The software analyst says, 'Let's push it back up the hill and see if it does it "
                           "again.'", user="Dhileas", date="2021-01-22", version=0)

entry_2 = EntryObject(tags=["test", "joke", "practice"], project_tags=["doris", "geraldine"],
                      body="A guy walks into a bar and asks for 1.4 root beers. The bartender says 'I'll have to charge"
                           " you extra, that's a root beer float'. The guy says 'In that case, better make it a "
                           "double.'", user="Dhileas", date="2021-01-22", version=0)

entry_3 = EntryObject(tags=["test", "fake", "joke", "practice"], project_tags=["doris", "horatio"],
                      body="Q: How many programmers does it take to screw in a light bulb? A: None. It's a hardware "
                           "problem.", user="Dhileas", date="2021-01-22", version=0)

entry_4 = EntryObject(tags=["test", "joke", "practice"], project_tags=["doris"],
                      body="In order to understand recursion you must first understand recursion.", user="Dhileas",
                      date="2021-01-22", version=0)

entry_5 = EntryObject(tags=["test", "fake", "joke", "practice"], project_tags=["doris", "geraldine", "horatio"],
                      body="Two bytes meet.  The first byte asks, 'Are you ill?' The second byte replies, 'No, just "
                           "feeling a bit off.'", user="Dhileas", date="2021-01-22", version=0)

entry_1.create()
entry_2.create()
entry_3.create()
entry_4.create()
entry_5.create()

# wait for the index so we can retrieve entry IDs # todo: the 201 response might return the IDs in the previous step
time.sleep(5)

section_1 = SectionObject(title="section_1", tags=["test", "joke", "practice"], project_tags=["doris", "geraldine"],
                           body=" A manager, a mechanical engineer, and software analyst are driving back from "
                                "convention through the mountains. Suddenly, as they crest a hill, the brakes on the "
                                "car go out and they fly careening down the mountain. After scraping against numerous "
                                "guardrails, they come to a stop in the ditch. Everyone gets out of the car to assess "
                                "the damage. The manager says, 'Let's form a group to collaborate ideas on how we can "
                                "solve this issue.' The mechanical engineer suggests, 'We should disassemble the car "
                                "and analyze each part for failure.' The software analyst says, 'Let's push it back up "
                                "the hill and see if it does it again.' \n\n  A guy walks into a bar and asks for 1.4 "
                                "root beers. The bartender says 'I'll have to charge you extra, that's a root beer "
                                "float'. The guy says 'In that case, better make it a double.'",
                           entries=[get_id(search(es_type="entry",
                                                  query=make_query(search_type="body",
                                                                   search_text=" A manager, a mechanical engineer, and "
                                                                               "software analyst are driving back from "
                                                                               "convention through the mountains. "
                                                                               "Suddenly, as they crest a hill, the "
                                                                               "brakes on the car go out and they fly "
                                                                               "careening down the mountain. After "
                                                                               "scraping against numerous guardrails, "
                                                                               "they come to a stop in the ditch. "
                                                                               "Everyone gets out of the car to assess "
                                                                              "the damage. The manager says, 'Let's "
                                                                              "form a group to collaborate ideas on how"
                                                                              " we can solve this issue.' The "
                                                                              "mechanical engineer suggests, 'We should"
                                                                              " disassemble the car and analyze each "
                                                                              "part for failure.' The software analyst "
                                                                              "says, 'Let's push it back up the hill "
                                                                              "and see if it does it again.'" ))),
                                   get_id(search(es_type="entry",
                                                 query=make_query(search_type="body",
                                                                  search_text="A guy walks into a bar and asks for 1.4 "
                                                                              "root beers. The bartender says 'I'll "
                                                                              "have to charge you extra, that's a root "
                                                                              "beer float'. The guy says 'In that case,"
                                                                              " better make it a double.'")))],
                          user="Dhileas",
                          date="2021-01-22", version=0)

section_2 = SectionObject(title="section_2", tags=["test", "joke"], project_tags=["doris", "horatio"],
                          body="Two bytes meet.  The first byte asks, 'Are you ill?' The second byte replies, 'No, "
                               "just feeling a bit off.' \n\nQ: How many programmers does it take to screw in a light "
                               "bulb? A: None. It's a hardware problem.",
                          entries=[get_id(search(es_type="entry",
                                                 query=make_query(search_type="body",
                                                                  search_text="Two bytes meet.  The first byte asks, "
                                                                              "'Are you ill?' The second byte replies, "
                                                                              "'No, just feeling a bit off.'"))),
                                   get_id(search(es_type="entry",
                                                 query=make_query(search_type="body",
                                                                  search_text="Q: How many programmers does it take to "
                                                                              "screw in a light bulb? A: None. It's a "
                                                                              "hardware problem.")))],
                          user="Dhileas", date="2021-01-22", version=0)

section_3 = SectionObject(title="section_3", tags=["test", "fake news"], project_tags=["doris"],
                          body="In order to understand recursion you must first understand recursion.",
                          entries=[get_id(search(es_type="entry",
                                                 query=make_query(search_type="body",
                                                                  search_text="In order to understand recursion you "
                                                                              "must first understand recursion.")))],
                          user="Dhileas", date="2021-01-22", version=0)

#
section_1.create()
section_2.create()
section_3.create()

time.sleep(5)

# purposely not writing the body in markdown, so that they can be updated later. I didn't want to deal with the
# formatting just now, I just want something to test with
bid_1 = BidObject(title="pearl", body="In order to understand recursion you must first understand recursion. \n\nTwo "
                                      "bytes meet.  The first byte asks, 'Are you ill?' The second byte replies, 'No, "
                                      "just feeling a bit off.' \n\nQ: How many programmers does it take to screw in a "
                                      "light bulb? A: None. It's a hardware problem.",
                  sections=[get_id(search(es_type="section",
                                          query=make_query(search_type="body",
                                                           search_text="In order to understand recursion you "))),
                            get_id(search(es_type="section",
                                          query=make_query(search_type="body",
                                                           search_text="feeling a bit off.' \n\nQ: How many")))],
                  user="Dhileas", date="2021-01-22", version=0)

bid_2 = BidObject(title="barbara",
                  body=" A manager, a mechanical engineer, and software analyst are driving back from convention "
                       "through the mountains. Suddenly, as they crest a hill, the brakes on the car go out and they "
                       "fly careening down the mountain. After scraping against numerous guardrails, they come to a "
                       "stop in the ditch. Everyone gets out of the car to assess the damage. The manager says, 'Let's"
                       " form a group to collaborate ideas on how we can solve this issue.' The mechanical engineer "
                       "suggests, 'We should disassemble the car and analyze each part for failure.' The software "
                       "analyst says, 'Let's push it back up the hill and see if it does it again.' \n\n  A guy walks "
                       "into a bar and asks for 1.4 root beers. The bartender says 'I'll have to charge you extra, "
                       "that's a root beer float'. The guy says 'In that case, better make it a double.' \n\nTwo bytes "
                       "meet.  The first byte asks, 'Are you ill?' The second byte replies, 'No, just feeling a bit "
                       "off.' \n\nQ: How many programmers does it take to screw in a light bulb? A: None. It's a "
                       "hardware problem.",
                  sections=[get_id(search(es_type="section",
                                          query=make_query(search_type="body",
                                                           search_text="The software analyst says, 'Let's push it back "
                                                                       "up the hill and see if it does it again.' "
                                                                       "\n\n  A guy walks into a"))),
                            get_id(search(es_type="section",
                                          query=make_query(search_type="body",
                                                           search_text="feeling a bit off.' \n\nQ: How many")))],
                  user="Dhileas", date="2021-01-22", version=0)

bid_1.create()
bid_2.create()
