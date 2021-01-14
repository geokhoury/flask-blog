from mongoengine import *


class User(Document):
    # define class metadata
    meta = {'collection': 'users'}

    # define class fields
    username = StringField(required=True)
    password = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
    biography = StringField(max_length=50)
