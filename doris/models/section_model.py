from doris.models.es_object import ElasticsearchObject
# Importing the parent class that the entry class will inherit its elasticsearch functionality from


# for some reason the ElasticsearchObject won't autocomplete. Not sure if that means it's broken
class SectionObject(ElasticsearchObject):
    def __init__(self, **kwargs):
        self.title = kwargs["title"]
        self.tags = kwargs["tags"]
        self.project_tags = kwargs["project_tags"]
        self.body = kwargs["body"]
        self.entries = kwargs["entries"]
        self.user = kwargs["user"]
        self.date = kwargs["date"]
        self.version = kwargs["version"]

    @property
    def title(self):
        return self.title

    @title.setter
    def title(self, value: str):  # this is a type annotation.
        self.title = value

    @property
    def tags(self):
        return self.tags

    @tags.setter
    def tags(self, value: str):
        self.tags = value

    @property
    def project_tags(self):
        return self.project_tags

    @project_tags.setter
    def project_tags(self, value: str):
        self.project_tags = value

    @property
    def body(self):
        return self.body

    @body.setter
    def body(self, value):
        self.body = value

    @property
    def entries(self):
        return self.entries

    @entries.setter
    def entries(self, value):
        self.entries = value

    @property
    def user(self):
        return self.user

    @user.setter
    def user(self, value):
        self.user = value

    # I think version's going to be a bit different. I'm going to want to check whether there is a current version, and
    # if not, make one. If there is, the version number is going to be n + 1. I'll come back to this.
    @property
    def version(self):
        return self.version

    @version.setter
    def version(self, value):
        self.version = value

    @property
    def date(self):
        return self.date

    @date.setter
    def date(self, value):
        self.date = value
