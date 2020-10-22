from doris.models.es_object import ElasticsearchObject
import requests
# Importing the parent class that the entry class will inherit its elasticsearch functionality from


class Bid(ElasticsearchObject):
    es_type = "bid"

    def __init__(self, **kwargs):
        super(Bid, self).__init__(**kwargs)
        if self.data is None:
            self.data = {}
        self.data["title"] = kwargs["title"]
        self.data["body"] = kwargs["body"]
        self.data["sections"] = kwargs["sections"]
        self.data["user"] = kwargs["user"]
        self.data["date"] = kwargs["date"]
        self.data["version"] = kwargs["version"]

    @property
    def title(self):
        return self.data["title"]

    @title.setter
    def title(self, value: str):  # this is a type annotation.
        self.data["title"] = value

    @property
    def body(self):
        return self.data["body"]

    @body.setter
    def body(self, value):
        self.data["body"] = value

    @property
    def sections(self):
        return self.data["entries"]

    @sections.setter
    def sections(self, value):
        self.data["entries"] = value

    @property
    def user(self):
        return self.data["user"]

    @user.setter
    def user(self, value):
        self.data["user"] = value

    # I think version's going to be a bit different. I'm going to want to check whether there is a current version, and
    # if not, make one. If there is, the version number is going to be n + 1. I'll come back to this.
    @property
    def version(self):
        return self.data["version"]

    @version.setter
    def version(self, value):
        self.data["version"] = value

    @property
    def date(self):
        return self.data["date"]

    @date.setter
    def date(self, value):
        self.data["date"] = value
