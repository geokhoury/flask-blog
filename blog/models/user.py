from mongoengine import *
from bson import ObjectId
from passlib.hash import pbkdf2_sha256

class User(Document):
    # define class metadata
    meta = {'collection': 'users'}

    # define class fields
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    role = IntField(default=0)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
    biography = StringField(max_length=50)
    favorites = ListField(StringField())

    # define class methods

    # this method authenticates the user using credentials
    def authenticate(self, username, password):
        # username / password -> from the login form
        # self.username / self.password -> from the database
        if username == self.username and pbkdf2_sha256.verify(password, self.password):
            return True
        else:
            return False

    def encrypt_password(self, password):
        return pbkdf2_sha256.hash(password)

    # this method changes the user password
    def change_password(self, current_password, new_password):
        if current_password == self.password:
            self.password = self.encrypt_password(new_password)

    # this method serializes the object into a JSON object
    def serialize(self):
        serialized = {
            "id": str(self.pk),
            'username': self.username,
            'password': 'nice try :)!',
            'role': self.role,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'biography': self.biography
        }

        return serialized
