import requests
from doris import app
import json
# The basic class of an elasticsearch object.
# This will be the parent class for entries, sections and bids, as well as images

# we need a URL first. Where is the ES database going to be stored????? But I digress.

class ElasticsearchObject(object):
    def __init__(self, **kwargs):
        pass

    es_type = None
    data = None

    def create(self):
        url = app.config.get("ELASTICSEARCH_URL") + self.es_type + "/"

        payload = json.dumps(self.data)
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response

    @classmethod
    def retrieve(cls, _id):
        url = app.config.get("ELASTICSEARCH_URL") + cls.es_type + "/" + _id

        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers)

        return cls(**response.json()["_source"])

    def update(self, new_body):
        url = app.config.get("ELASTICSEARCH_URL") + self.es_type + "/" + self.data["id"]
        # version_url = app.config.get("VERSION_URL") + self.es_type + "/"
        # need to save a copy of the previous versions in a version index

        self.data["body"] = new_body
        payload = json.dumps(self.data)
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)

        return response



    def delete(self, _id):
        url = app.config.get("ELASTICSEARCH_URL") + self.es_type + "/" + _id
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("DELETE", url, headers=headers)
        return response

    def search(self, query):
        url = app.config.get("ELASTICSEARCH_URL") + self.es_type + "/_search"

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
