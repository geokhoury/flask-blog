from mongoengine import *
from .comment import Comment
from .user import User
from datetime import datetime
from bson import ObjectId
from flask import session


class PostQuerySet(QuerySet):

    def get_new_posts(self):
        return self.filter(published=True).order_by('-published_at')

    def get_trending_posts(self):
        return self.filter(published=True).order_by('-view_count')

    def get_published(self):
        return self.filter(published=True)

    def get_published_by_user(self):
        return self.filter(published=True, author=ObjectId(session['user']['id'])).order_by('-published_at')

    def get_user_drafts(self):
        return self.filter(published=False, author=ObjectId(session['user']['id']))

    def get_user_favorites(self):
        # get list of user favorite post ids
        favorite_post_ids = User.objects(id=session['user']['id']).get().favorites

        # filter the queryset
        return self.filter(id__in=favorite_post_ids)


class Post(Document):
    # define class metadata
    meta = {'collection': 'posts',
            'queryset_class': PostQuerySet, 'allow_inheritance': True,
            }

    # define class fields
    title = StringField(max_length=120, required=True)
    author = ReferenceField(User)
    tags = ListField(StringField(max_length=30))
    comments = ListField(EmbeddedDocumentField(Comment))
    created_at = DateTimeField(default=datetime.now())
    published_at = DateTimeField()
    view_count = IntField(default=0)
    published = BooleanField(default=False)

    def publish(self):
        self.published = True
        self.published_at = datetime.now()
        self.save()


class TextPost(Post):

    meta = {'indexes':
            [
                {'fields': ['$title', '$content'],
                 'default_language': 'english',
                 'weights': {'title': 10, 'content': 2}
                 }
            ]}
    content = StringField()


class ImagePost(Post):
    image_path = StringField()


class LinkPost(Post):
    link_url = StringField()
