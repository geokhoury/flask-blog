import os

from flask import Flask
from mongoengine import *
from blog.models import *
import json

def create_app(test_config=None):
    # create the Flask
    app = Flask(__name__, instance_relative_config=True)

    # configure the app
    app.config.from_mapping(
        SECRET_KEY='dev',
        MONGO_URI="mongodb://root:example@localhost:27017/blog?authSource=admin"
    )

    # connect to MongoDB using mongoengine
    connect(
        db='blog',
        username='root',
        password='example',
        authentication_source='admin'
    )

    # define our collections
    # users = mongo.blog.users

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, world!'

    @app.route('/test-db')
    def test_db():
        bert = User(email='bert@sesame.com', first_name='Bert',
                    last_name='Sesame').save()

        cookie = User(email='cookie@monster.com', first_name='Cookie',
                    last_name='Monster').save()
        # Create TextPost
        post1 = TextPost(title='Fun with MongoEngine', author=cookie)

        post1.content = 'Took a look at MongoEngine today, looks pretty cool.'
        post1.tags = ['mongodb', 'mongoengine']
        post1.save()

        # Create LinkPost
        post2 = LinkPost(title='MongoEngine Documentation', author=bert)
        post2.link_url = 'http://docs.mongoengine.com/'
        post2.tags = ['mongoengine']
        post2.save()

        # for post in Post.objects:
        #     print(post.title)

        return TextPost.objects()

    # register the 'post' blueprint
    from .blueprints.post import post_bp
    app.register_blueprint(post_bp)

    # register the 'user' blueprint
    from .blueprints.user import user_bp
    app.register_blueprint(user_bp)

    # register the 'login' blueprint
    from .blueprints.login import login_bp
    app.register_blueprint(login_bp)

    return app
