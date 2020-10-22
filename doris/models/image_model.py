from doris.models.es_object import ElasticsearchObject
# Importing the parent class that the entry class will inherit its elasticsearch functionality from


# **kwargs is probably useful here. Figure it out

class Image(ElasticsearchObject):
    es_type = "image"

    def __init__(self, **kwargs):
        super(Image, self).__init__(**kwargs)
        if self.data is None:
            self.data = {}
        self.data["title"] = kwargs["title"]
        self.data["url"] = kwargs["url"]
        self.data["alt_text"] = kwargs["alt_text"]
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
    def url(self):
        return self.data["url"]

    @url.setter
    def url(self, value: str):
        self.data["url"] = value

    @property
    def alt_text(self):
        return self.data["alt_text"]

    @alt_text.setter
    def alt_text(self, value: str):
        self.data["alt_text"] = value

    @property
    def user(self):
        return self.data["user"]

    @user.setter
    def user(self, value):
        self.data["user"] = value

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
