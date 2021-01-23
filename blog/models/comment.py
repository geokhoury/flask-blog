from mongoengine import *


class Comment(EmbeddedDocument):
    content = StringField()
    name = StringField(max_length=120)
    