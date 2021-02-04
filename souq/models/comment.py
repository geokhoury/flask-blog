from mongoengine import *
from .user import User


class Comment(EmbeddedDocument):
    content = StringField()
    # name = StringField(max_length=120)
    author = ReferenceField(User)
