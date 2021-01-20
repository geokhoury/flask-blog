from mongoengine import *
from .comment import Comment
from .user import User
from datetime import datetime

class Post(Document):
    # define class metadata
    meta = {'collection': 'posts', 'allow_inheritance': True}

    # define class fields
    title = StringField(max_length=120, required=True)
    author = ReferenceField(User)
    tags = ListField(StringField(max_length=30))
    comments = ListField(EmbeddedDocumentField(Comment))
    created_at = DateTimeField(default=datetime.now())
    published = BooleanField(default = False)
    published_at=DateField(default=None)

class TextPost(Post):
    content = StringField()

    @queryset_manager
    def get_published_posts(self, doc_cls, queryset):
        return queryset.filter(published = True)

    @queryset_manager
    def get_recent_posts(self, doc_cls, queryset):
        return queryset.order_by("-created_at")
    
    # def publish(self):
    #     self.published=True
    #     self.published_at=datetime.now()



class ImagePost(Post):
    image_path = StringField()


class LinkPost(Post):
    link_url = StringField()
