import datetime
import pymongo


class DbManip():
    def __init__(self):
        self.mongodb = pymongo.MongoClient()
        self.lofann_db = self.mongodb.lofann_database
        self.items = self.lofann_db.items

    def add_announcement(self, title, announcement):
        item = {
            'title': title,
            'announcement': announcement,
            'created_at': datetime.datetime.utcnow()
        }
        self.items.insert(item)

    def get_announcements(self):
        return self.items.find().sort('created_at', pymongo.DESCENDING)
