import requests
import json
from datetime import date
# The basic class of an elasticsearch object.
# This will be the parent class for entries, sections and bids, as well as images


ELASTICSEARCH_URL = "http://localhost:9200/test_one_doris-"
VERSION_URL = "http://localhost:9200/version/"


class ElasticsearchObject(object):
    def __init__(self, **kwargs):
        pass

    es_type = None
    data = None

    def create(self):
        url = ELASTICSEARCH_URL + self.es_type + "/_create/" + str(self.data["id"])


        payload = json.dumps(self.data)
        print(payload)
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("PUT", url, headers=headers, data=payload)
        print(response)

        return response

    @classmethod
    def retrieve(cls, _id):
        url = ELASTICSEARCH_URL + cls.es_type + "/_doc/" + _id

        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("GET", url, headers=headers)

        if response.status_code == 200:

            return cls(**response.json()["_source"])

        return None

    def update(self, **kwargs):
        url = ELASTICSEARCH_URL + self.es_type + "/_doc/" + self.data["id"]
        # version_url = app.config.get("VERSION_URL") + self.es_type + "/"
        # need to save a copy of the previous versions in a version index
        # Changed to kwargs because tags and project tags may need to be updated

        self.data["tags"] = kwargs["new_tags"]
        self.data["project_tags"] = kwargs["new_project_tags"]
        self.data["body"] = kwargs["new_body"]
        self.data["version"] = self.data["version"] + 1
        payload = json.dumps(self.data)
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)

        return response

    def delete(self, _id):
        url = ELASTICSEARCH_URL + self.es_type + "/_doc/" + _id
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("DELETE", url, headers=headers)
        return response

    @classmethod
    def search(cls, query=None):
        if query is None:
            query = {"query": {"match_all": {}}}
        url = ELASTICSEARCH_URL + cls.es_type + "/_search"

        payload = json.dumps(query)
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        return response

# The model needs to have functions that allow elasticsearch integration, which will include:
# POSTing the data to elasticsearch both to add and update an entry. Will need to check version number.
# GETting the data from elasticsearch as part of a search. This will involve different types of query depending on
# which checkboxes are ticked in the searchbar.
