from mongoengine import *
from mongoengine.fields import DateField
from .comment import Comment
from .user import User
from datetime import datetime

class Post(Document):
    # define class metadata
    meta = {'collection': 'posts', 'allow_inheritance': True}
    # define class fields
    title = StringField(max_length=120, required=True)
    author = ReferenceField(User,reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=30))
    comments = ListField(EmbeddedDocumentField(Comment))
    created_at = DateTimeField(default=datetime.now())

class TextPost(Post):
    content = StringField()


class ImagePost(Post):
    image_path = StringField()


class LinkPost(Post):
    link_url = StringField()
