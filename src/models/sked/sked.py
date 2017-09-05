import uuid
from operator import itemgetter
import src.models.sked.constants as SkedConstants
from src.common.database import Database


class Sked(object):
    def __init__(self, user_email, day, time, name, active=True, _id=None):
        self.user_email = user_email
        self.day = day
        self.time = time
        self.name = name
        self._id = uuid.uuid4().hex if _id is None else _id
        self.active = active

    def __repr__(self):
        return "<Sked {} for {} on {} at {}>".format(self.name, self.user_email, self.day, self.time)

    def save(self):
        Database.update(SkedConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            "_id": self._id,
            "user_email": self.user_email,
            "name": self.name,
            "day": self.day,
            "time": self.time,
            "active": self.active
        }

    @classmethod
    def find_by_email(cls, user_email):
        return sorted([cls(**sked) for sked in Database.find(SkedConstants.COLLECTION, {"user_email": user_email})], key=lambda sked: sked.time)

    @classmethod
    def find_by_id(cls, sked_id):
        return cls(**Database.find_one(SkedConstants.COLLECTION, {"_id": sked_id}))

    def deactivate(self):
        self.active = False
        self.save()

    def activate(self):
        self.active = True
        self.save()

    def delete(self):
        Database.remove(SkedConstants.COLLECTION, {"_id": self._id})
