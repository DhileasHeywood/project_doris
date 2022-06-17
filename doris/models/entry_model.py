from doris.models.es_object import ElasticsearchObject
# Importing the parent class that the entry class will inherit its elasticsearch functionality from
from uuid import uuid4



class Entry(ElasticsearchObject):
    es_type = "entry"

    def __init__(self, **kwargs):
        super(Entry, self).__init__(**kwargs)
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
        else:
            self.data["id"] = str(uuid4())

    @property
    def tags(self):
        return self.data["tags"]

    @tags.setter
    def tags(self, value: str):
        self.data["tags"] = value

    @property
    def project_tags(self):
        return self.data["project_tags"]

    @project_tags.setter
    def project_tags(self, value: str):
        self.data["project_tags"] = value

    @property
    def body(self):
        return self.data["body"]

    @body.setter
    def body(self, value):
        self.data["body"] = value

    @property
    def entries(self):
        return self.data["entries"]

    @entries.setter
    def entries(self, value):
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
