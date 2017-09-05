import uuid
from src.common.database import Database
from src.common.utils import Utils
import src.models.users.errors as UserErrors
import src.models.users.constants as UserConstants
from src.models.sked.sked import Sked


class User(object):
    def __init__(self, email, password, name, _id=None):
        self.name = name
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<User: {}".format(self.email)

    @staticmethod
    def login_valid(email, password):
        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})
        if user_data is None:
            raise UserErrors.UserNotExistError("Your user does not exist")
        if not Utils.check_hashed_password(password, user_data['password']):
            raise UserErrors.IncorrectPasswordError("Your password was wrong")
        return True

    @staticmethod
    def register_user(email, password, name):
        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})
        if user_data is not None:
            raise UserErrors.UserAlreadyRegisteredError("Email already exists")
        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError("The email address is invalid")
        User(email, Utils.hash_password(password), name).save()
        return True

    def save(self):
        Database.insert(collection=UserConstants.COLLECTION,
                        data=self.json())

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "email": self.email,
            "password": self.password
        }

    @classmethod
    def find_by_email(cls, email):
        return cls(**(Database.find_one(collection=UserConstants.COLLECTION, query={"email": email})))

    def get_sked(self):
        return Sked.find_by_email(self.email)