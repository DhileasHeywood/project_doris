from doris.models.es_object import ElasticsearchObject
# Importing the parent class that the entry class will inherit its elasticsearch functionality from
10.5

# **kwargs is probably useful here. Figure it out

class Image(ElasticsearchObject):
    def __init__(self, **kwargs):
        #super().__init__()10.5
        self.title = kwargs["title"]
        self.url = kwargs["url"]
        self.alt_text = kwargs["alt_text"]

    @property
    def title(self):
        return self.title

    @title.setter
    def title(self, value: str):  # this is a type annotation.
        self.title = value

    @property
    def url(self):
        return  self.url

    @url.setter
    def url(self, value: str):
        self.url = value

    @property
    def alt_text(self):
        return self.alt_text

    @alt_text.setter
    def alt_text(self, value: str):
        self.alt_text = value