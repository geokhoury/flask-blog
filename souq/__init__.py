from flask import Flask
from souq.models import *
from flask_hashing import Hashing
import json
from flask_scss import Scss
from flask_assets import Environment, Bundle
from mongoengine import *
import os


def create_app(test_config=None):
    # create the Flask
    app = Flask(__name__, instance_relative_config=True)
    # instance for scss
    assets = Environment(app)
    assets.url = app.static_url_path
    scss = Bundle('index.scss', filters='scss', output='index.css')
    assets.register('scss_all', scss)
    assets.init_app(app)
    hashing = Hashing(app)
    # configure the app
    app.config.from_mapping(
        SECRET_KEY='dev',
        MONGO_URI="mongodb://root:example@localhost:27017/souq?authSource=admin"
    )

    # connect to MongoDB using mongoengine
    connect(
        db='souq',
    )


    @app.route('/test-db')
    def test_db():
        bert = User(username='bert',password='1234', first_name='Bert',
                    last_name='Sesame').save()

        cookie = User(username='cookie@monster.com',password='258', first_name='Cookie',
                    last_name='Monster').save()
        c1 = Comment(content='test comment 1',author=bert)
        c2 = Comment(content='test comment 2',author=cookie)

        # Create Textitem
        item1 = TextItem(title='Fun with MongoEngine', author=bert,comments= [c1,c2])

        item1.content = 'Took a look at MongoEngine today, looks pretty cool.'
        item1.tags = ['mongodb', 'mongoengine']
        item1.save()

        # Create Linkitem
        item2 = LinkItem(title='MongoEngine Documentation', author=bert)
        item2.link_url = 'http://docs.mongoengine.com/'
        item2.tags = ['mongoengine']
        item2.save()

        # for item in item.objects:
        #     print(item.title)

        return 'data base'

    # register the 'item' blueprint
    from .blueprints.item import item_bp
    app.register_blueprint(item_bp)

    # register the 'user' blueprint
    from .blueprints.user import user_bp
    app.register_blueprint(user_bp)

    # register the 'login' blueprint
    from .blueprints.login import login_bp
    app.register_blueprint(login_bp)

    return app
