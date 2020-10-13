# The basic class of an elasticsearch object.
# This will be the parent class for entries, sections and bids, as well as images

class ElasticsearchObject:
    def __init__(self):
        pass


# The model needs to have functions that allow elasticsearch integration, which will include:
# POSTing the data to elasticsearch both to add and update an entry. Will need to check version number.
# GETting the data from elasticsearch as part of a search. This will involve different types of query depending on
# which checkboxes are ticked in the searchbar.
