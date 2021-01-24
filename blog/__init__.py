import os
import json

from flask import Flask, session, redirect, url_for, request
from functools import wraps
from mongoengine import *
from blog.models import User, TextPost, Post
from datetime import datetime
from passlib.hash import pbkdf2_sha256

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user') is None:
            return redirect(url_for('login.login'))
        return f(*args, **kwargs)
    return decorated_function


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
        host='mongo',
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

    @app.route('/dummy/init-db')
    def init_db():

        # drop collection before initialization
        User.drop_collection()
        Post.drop_collection()

        common_password = pbkdf2_sha256.hash('1234')

        bert = User(username='bert', password=common_password, first_name='Bert',
                    last_name='Sesame').save()

        cookie = User(username='cookie', password=common_password,
                      first_name='Cookie', last_name='Monster').save()

        # Create TextPost
        post1 = TextPost(title='Fun with MongoEngine',
                         author=cookie, published=True)
        post1.published_at = datetime.now()
        post1.content = 'Nulla venenatis, nisi et semper pharetra, augue orci consectetur enim, ullamcorper porta metus nunc nec risus. Vestibulum id lacus sed erat tempus elementum a et est. Nulla tincidunt molestie fermentum. Ut mattis diam nec augue volutpat, eu molestie libero bibendum. Sed tempus diam non interdum euismod. Aliquam aliquam maximus tincidunt. Ut suscipit, erat ut aliquam dignissim, augue nibh aliquam nunc, a porta tellus massa nec erat. Integer ultrices, leo ut feugiat maximus, ipsum erat porttitor est, nec mollis ipsum odio ac nisi. In suscipit leo eget facilisis malesuada. Cras mollis vitae odio at maximus. Nulla nunc libero, sodales quis purus a, lobortis dapibus felis. Donec aliquet varius sapien ut tristique. Sed eros turpis, sodales eget tristique non, consequat id mi. Vestibulum risus nisl, gravida eget convallis maximus, sagittis quis metus. Nam hendrerit elit tellus, non euismod nisl sagittis non. Curabitur pharetra massa nec tortor convallis hendrerit. Ut a sodales felis. Nullam euismod ipsum ac quam lacinia, nec elementum ex fringilla. Vestibulum et lectus libero. Aliquam non malesuada ante, venenatis imperdiet quam. Pellentesque auctor interdum justo, sit amet rutrum enim consequat sed. Suspendisse in est nibh. Pellentesque vitae mattis quam. Curabitur elementum volutpat sollicitudin. Sed eleifend sapien vitae felis interdum, at tincidunt nibh convallis. Pellentesque in ullamcorper lectus. Quisque bibendum rutrum lacus vel consequat. Curabitur lacinia ornare dignissim. Suspendisse pharetra vel lorem nec ultricies. Vivamus vitae tortor et ante posuere ornare. Curabitur mollis sapien vitae auctor accumsan. Nam venenatis neque eu malesuada sagittis. Suspendisse volutpat feugiat sapien. Sed convallis ex vel nibh blandit, vitae elementum eros imperdiet. Suspendisse blandit interdum justo, ac condimentum ipsum. Donec aliquam porta magna. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc elementum velit eu erat porttitor porttitor a ac dolor. In hac habitasse platea dictumst. Aenean ex velit, malesuada at venenatis nec, venenatis quis odio. Vestibulum pulvinar elementum rhoncus. Cras maximus dolor quam, eu venenatis velit dignissim vitae. Sed elit ex, pellentesque vitae euismod in, venenatis sed mauris. Donec porttitor semper pellentesque. Nunc condimentum magna urna, quis ultricies justo ullamcorper id. Donec facilisis et orci quis venenatis. Nulla id tempus libero. Praesent hendrerit euismod mattis. Donec convallis neque congue ante laoreet, at hendrerit dui euismod. Sed nec sollicitudin lorem. Praesent tincidunt justo eget nisi efficitur, eu semper urna feugiat. Nunc ipsum velit, pretium nec eleifend vitae, vestibulum eget mi. Suspendisse faucibus a felis in gravida. Maecenas fringilla lorem diam, in tempus nisl ultricies et. Sed elit mauris, hendrerit eu ullamcorper nec, auctor sed velit. In eget lectus pharetra, dignissim nisi id, consequat orci. Etiam rhoncus lacinia dignissim. Proin pretium nunc at nisl imperdiet, eget aliquet quam interdum. Proin sit amet porttitor libero. Nullam sit amet rhoncus sem. Morbi lobortis enim in mauris molestie vestibulum. Phasellus nec metus et dolor egestas ultrices. Vivamus in massa odio. Nullam ac erat at nisi faucibus maximus. Vivamus est purus, eleifend ornare eros quis, vulputate auctor nibh. Pellentesque vehicula lorem in ornare porta. Nam tristique, nisl sit amet porta pretium, nunc dui blandit nulla, fermentum efficitur neque lorem vel eros.'
        post1.tags = ['mongodb', 'mongoengine']
        post1.save()

        post2 = TextPost(title='Fun with MongoEngine.',
                         author=cookie, published=True)
        post2.published_at = datetime.now()
        post2.content = 'Nulla venenatis, nisi et semper pharetra, augue orci consectetur enim, ullamcorper porta metus nunc nec risus. Vestibulum id lacus sed erat tempus elementum a et est. Nulla tincidunt molestie fermentum. Ut mattis diam nec augue volutpat, eu molestie libero bibendum. Sed tempus diam non interdum euismod. Aliquam aliquam maximus tincidunt. Ut suscipit, erat ut aliquam dignissim, augue nibh aliquam nunc, a porta tellus massa nec erat. Integer ultrices, leo ut feugiat maximus, ipsum erat porttitor est, nec mollis ipsum odio ac nisi. In suscipit leo eget facilisis malesuada. Cras mollis vitae odio at maximus. Nulla nunc libero, sodales quis purus a, lobortis dapibus felis. Donec aliquet varius sapien ut tristique. Sed eros turpis, sodales eget tristique non, consequat id mi. Vestibulum risus nisl, gravida eget convallis maximus, sagittis quis metus. Nam hendrerit elit tellus, non euismod nisl sagittis non. Curabitur pharetra massa nec tortor convallis hendrerit. Ut a sodales felis. Nullam euismod ipsum ac quam lacinia, nec elementum ex fringilla. Vestibulum et lectus libero. Aliquam non malesuada ante, venenatis imperdiet quam. Pellentesque auctor interdum justo, sit amet rutrum enim consequat sed. Suspendisse in est nibh. Pellentesque vitae mattis quam. Curabitur elementum volutpat sollicitudin. Sed eleifend sapien vitae felis interdum, at tincidunt nibh convallis. Pellentesque in ullamcorper lectus. Quisque bibendum rutrum lacus vel consequat. Curabitur lacinia ornare dignissim. Suspendisse pharetra vel lorem nec ultricies. Vivamus vitae tortor et ante posuere ornare. Curabitur mollis sapien vitae auctor accumsan. Nam venenatis neque eu malesuada sagittis. Suspendisse volutpat feugiat sapien. Sed convallis ex vel nibh blandit, vitae elementum eros imperdiet. Suspendisse blandit interdum justo, ac condimentum ipsum. Donec aliquam porta magna. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc elementum velit eu erat porttitor porttitor a ac dolor. In hac habitasse platea dictumst. Aenean ex velit, malesuada at venenatis nec, venenatis quis odio. Vestibulum pulvinar elementum rhoncus. Cras maximus dolor quam, eu venenatis velit dignissim vitae. Sed elit ex, pellentesque vitae euismod in, venenatis sed mauris. Donec porttitor semper pellentesque. Nunc condimentum magna urna, quis ultricies justo ullamcorper id. Donec facilisis et orci quis venenatis. Nulla id tempus libero. Praesent hendrerit euismod mattis. Donec convallis neque congue ante laoreet, at hendrerit dui euismod. Sed nec sollicitudin lorem. Praesent tincidunt justo eget nisi efficitur, eu semper urna feugiat. Nunc ipsum velit, pretium nec eleifend vitae, vestibulum eget mi. Suspendisse faucibus a felis in gravida. Maecenas fringilla lorem diam, in tempus nisl ultricies et. Sed elit mauris, hendrerit eu ullamcorper nec, auctor sed velit. In eget lectus pharetra, dignissim nisi id, consequat orci. Etiam rhoncus lacinia dignissim. Proin pretium nunc at nisl imperdiet, eget aliquet quam interdum. Proin sit amet porttitor libero. Nullam sit amet rhoncus sem. Morbi lobortis enim in mauris molestie vestibulum. Phasellus nec metus et dolor egestas ultrices. Vivamus in massa odio. Nullam ac erat at nisi faucibus maximus. Vivamus est purus, eleifend ornare eros quis, vulputate auctor nibh. Pellentesque vehicula lorem in ornare porta. Nam tristique, nisl sit amet porta pretium, nunc dui blandit nulla, fermentum efficitur neque lorem vel eros.'
        post2.tags = ['mongoengine', 'flask']
        post2.save()

        post3 = TextPost(title='Mauris et rutrum nisl.',
                         author=bert, published=True)
        post3.published_at = datetime.now()
        post3.content = 'Nulla venenatis, nisi et semper pharetra, augue orci consectetur enim, ullamcorper porta metus nunc nec risus. Vestibulum id lacus sed erat tempus elementum a et est. Nulla tincidunt molestie fermentum. Ut mattis diam nec augue volutpat, eu molestie libero bibendum. Sed tempus diam non interdum euismod. Aliquam aliquam maximus tincidunt. Ut suscipit, erat ut aliquam dignissim, augue nibh aliquam nunc, a porta tellus massa nec erat. Integer ultrices, leo ut feugiat maximus, ipsum erat porttitor est, nec mollis ipsum odio ac nisi. In suscipit leo eget facilisis malesuada. Cras mollis vitae odio at maximus. Nulla nunc libero, sodales quis purus a, lobortis dapibus felis. Donec aliquet varius sapien ut tristique. Sed eros turpis, sodales eget tristique non, consequat id mi. Vestibulum risus nisl, gravida eget convallis maximus, sagittis quis metus. Nam hendrerit elit tellus, non euismod nisl sagittis non. Curabitur pharetra massa nec tortor convallis hendrerit. Ut a sodales felis. Nullam euismod ipsum ac quam lacinia, nec elementum ex fringilla. Vestibulum et lectus libero. Aliquam non malesuada ante, venenatis imperdiet quam. Pellentesque auctor interdum justo, sit amet rutrum enim consequat sed. Suspendisse in est nibh. Pellentesque vitae mattis quam. Curabitur elementum volutpat sollicitudin. Sed eleifend sapien vitae felis interdum, at tincidunt nibh convallis. Pellentesque in ullamcorper lectus. Quisque bibendum rutrum lacus vel consequat. Curabitur lacinia ornare dignissim. Suspendisse pharetra vel lorem nec ultricies. Vivamus vitae tortor et ante posuere ornare. Curabitur mollis sapien vitae auctor accumsan. Nam venenatis neque eu malesuada sagittis. Suspendisse volutpat feugiat sapien. Sed convallis ex vel nibh blandit, vitae elementum eros imperdiet. Suspendisse blandit interdum justo, ac condimentum ipsum. Donec aliquam porta magna. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc elementum velit eu erat porttitor porttitor a ac dolor. In hac habitasse platea dictumst. Aenean ex velit, malesuada at venenatis nec, venenatis quis odio. Vestibulum pulvinar elementum rhoncus. Cras maximus dolor quam, eu venenatis velit dignissim vitae. Sed elit ex, pellentesque vitae euismod in, venenatis sed mauris. Donec porttitor semper pellentesque. Nunc condimentum magna urna, quis ultricies justo ullamcorper id. Donec facilisis et orci quis venenatis. Nulla id tempus libero. Praesent hendrerit euismod mattis. Donec convallis neque congue ante laoreet, at hendrerit dui euismod. Sed nec sollicitudin lorem. Praesent tincidunt justo eget nisi efficitur, eu semper urna feugiat. Nunc ipsum velit, pretium nec eleifend vitae, vestibulum eget mi. Suspendisse faucibus a felis in gravida. Maecenas fringilla lorem diam, in tempus nisl ultricies et. Sed elit mauris, hendrerit eu ullamcorper nec, auctor sed velit. In eget lectus pharetra, dignissim nisi id, consequat orci. Etiam rhoncus lacinia dignissim. Proin pretium nunc at nisl imperdiet, eget aliquet quam interdum. Proin sit amet porttitor libero. Nullam sit amet rhoncus sem. Morbi lobortis enim in mauris molestie vestibulum. Phasellus nec metus et dolor egestas ultrices. Vivamus in massa odio. Nullam ac erat at nisi faucibus maximus. Vivamus est purus, eleifend ornare eros quis, vulputate auctor nibh. Pellentesque vehicula lorem in ornare porta. Nam tristique, nisl sit amet porta pretium, nunc dui blandit nulla, fermentum efficitur neque lorem vel eros.'
        post3.tags = ['mongoengine', 'flask', 'mongodb']
        post3.save()

        post4 = TextPost(title='Mauris et rutrum nisl.',
                         author=cookie, published=True)
        post4.published_at = datetime.now()
        post4.content = 'Nulla venenatis, nisi et semper pharetra, augue orci consectetur enim, ullamcorper porta metus nunc nec risus. Vestibulum id lacus sed erat tempus elementum a et est. Nulla tincidunt molestie fermentum. Ut mattis diam nec augue volutpat, eu molestie libero bibendum. Sed tempus diam non interdum euismod. Aliquam aliquam maximus tincidunt. Ut suscipit, erat ut aliquam dignissim, augue nibh aliquam nunc, a porta tellus massa nec erat. Integer ultrices, leo ut feugiat maximus, ipsum erat porttitor est, nec mollis ipsum odio ac nisi. In suscipit leo eget facilisis malesuada. Cras mollis vitae odio at maximus. Nulla nunc libero, sodales quis purus a, lobortis dapibus felis. Donec aliquet varius sapien ut tristique. Sed eros turpis, sodales eget tristique non, consequat id mi. Vestibulum risus nisl, gravida eget convallis maximus, sagittis quis metus. Nam hendrerit elit tellus, non euismod nisl sagittis non. Curabitur pharetra massa nec tortor convallis hendrerit. Ut a sodales felis. Nullam euismod ipsum ac quam lacinia, nec elementum ex fringilla. Vestibulum et lectus libero. Aliquam non malesuada ante, venenatis imperdiet quam. Pellentesque auctor interdum justo, sit amet rutrum enim consequat sed. Suspendisse in est nibh. Pellentesque vitae mattis quam. Curabitur elementum volutpat sollicitudin. Sed eleifend sapien vitae felis interdum, at tincidunt nibh convallis. Pellentesque in ullamcorper lectus. Quisque bibendum rutrum lacus vel consequat. Curabitur lacinia ornare dignissim. Suspendisse pharetra vel lorem nec ultricies. Vivamus vitae tortor et ante posuere ornare. Curabitur mollis sapien vitae auctor accumsan. Nam venenatis neque eu malesuada sagittis. Suspendisse volutpat feugiat sapien. Sed convallis ex vel nibh blandit, vitae elementum eros imperdiet. Suspendisse blandit interdum justo, ac condimentum ipsum. Donec aliquam porta magna. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc elementum velit eu erat porttitor porttitor a ac dolor. In hac habitasse platea dictumst. Aenean ex velit, malesuada at venenatis nec, venenatis quis odio. Vestibulum pulvinar elementum rhoncus. Cras maximus dolor quam, eu venenatis velit dignissim vitae. Sed elit ex, pellentesque vitae euismod in, venenatis sed mauris. Donec porttitor semper pellentesque. Nunc condimentum magna urna, quis ultricies justo ullamcorper id. Donec facilisis et orci quis venenatis. Nulla id tempus libero. Praesent hendrerit euismod mattis. Donec convallis neque congue ante laoreet, at hendrerit dui euismod. Sed nec sollicitudin lorem. Praesent tincidunt justo eget nisi efficitur, eu semper urna feugiat. Nunc ipsum velit, pretium nec eleifend vitae, vestibulum eget mi. Suspendisse faucibus a felis in gravida. Maecenas fringilla lorem diam, in tempus nisl ultricies et. Sed elit mauris, hendrerit eu ullamcorper nec, auctor sed velit. In eget lectus pharetra, dignissim nisi id, consequat orci. Etiam rhoncus lacinia dignissim. Proin pretium nunc at nisl imperdiet, eget aliquet quam interdum. Proin sit amet porttitor libero. Nullam sit amet rhoncus sem. Morbi lobortis enim in mauris molestie vestibulum. Phasellus nec metus et dolor egestas ultrices. Vivamus in massa odio. Nullam ac erat at nisi faucibus maximus. Vivamus est purus, eleifend ornare eros quis, vulputate auctor nibh. Pellentesque vehicula lorem in ornare porta. Nam tristique, nisl sit amet porta pretium, nunc dui blandit nulla, fermentum efficitur neque lorem vel eros.'
        post4.tags = ['mongodb', 'mongoengine']
        post4.save()

        post5 = TextPost(title='Mauris et rutrum nisl.',
                         author=cookie, published=True)
        post5.published_at = datetime.now()
        post5.content = 'Nulla venenatis, nisi et semper pharetra, augue orci consectetur enim, ullamcorper porta metus nunc nec risus. Vestibulum id lacus sed erat tempus elementum a et est. Nulla tincidunt molestie fermentum. Ut mattis diam nec augue volutpat, eu molestie libero bibendum. Sed tempus diam non interdum euismod. Aliquam aliquam maximus tincidunt. Ut suscipit, erat ut aliquam dignissim, augue nibh aliquam nunc, a porta tellus massa nec erat. Integer ultrices, leo ut feugiat maximus, ipsum erat porttitor est, nec mollis ipsum odio ac nisi. In suscipit leo eget facilisis malesuada. Cras mollis vitae odio at maximus. Nulla nunc libero, sodales quis purus a, lobortis dapibus felis. Donec aliquet varius sapien ut tristique. Sed eros turpis, sodales eget tristique non, consequat id mi. Vestibulum risus nisl, gravida eget convallis maximus, sagittis quis metus. Nam hendrerit elit tellus, non euismod nisl sagittis non. Curabitur pharetra massa nec tortor convallis hendrerit. Ut a sodales felis. Nullam euismod ipsum ac quam lacinia, nec elementum ex fringilla. Vestibulum et lectus libero. Aliquam non malesuada ante, venenatis imperdiet quam. Pellentesque auctor interdum justo, sit amet rutrum enim consequat sed. Suspendisse in est nibh. Pellentesque vitae mattis quam. Curabitur elementum volutpat sollicitudin. Sed eleifend sapien vitae felis interdum, at tincidunt nibh convallis. Pellentesque in ullamcorper lectus. Quisque bibendum rutrum lacus vel consequat. Curabitur lacinia ornare dignissim. Suspendisse pharetra vel lorem nec ultricies. Vivamus vitae tortor et ante posuere ornare. Curabitur mollis sapien vitae auctor accumsan. Nam venenatis neque eu malesuada sagittis. Suspendisse volutpat feugiat sapien. Sed convallis ex vel nibh blandit, vitae elementum eros imperdiet. Suspendisse blandit interdum justo, ac condimentum ipsum. Donec aliquam porta magna. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc elementum velit eu erat porttitor porttitor a ac dolor. In hac habitasse platea dictumst. Aenean ex velit, malesuada at venenatis nec, venenatis quis odio. Vestibulum pulvinar elementum rhoncus. Cras maximus dolor quam, eu venenatis velit dignissim vitae. Sed elit ex, pellentesque vitae euismod in, venenatis sed mauris. Donec porttitor semper pellentesque. Nunc condimentum magna urna, quis ultricies justo ullamcorper id. Donec facilisis et orci quis venenatis. Nulla id tempus libero. Praesent hendrerit euismod mattis. Donec convallis neque congue ante laoreet, at hendrerit dui euismod. Sed nec sollicitudin lorem. Praesent tincidunt justo eget nisi efficitur, eu semper urna feugiat. Nunc ipsum velit, pretium nec eleifend vitae, vestibulum eget mi. Suspendisse faucibus a felis in gravida. Maecenas fringilla lorem diam, in tempus nisl ultricies et. Sed elit mauris, hendrerit eu ullamcorper nec, auctor sed velit. In eget lectus pharetra, dignissim nisi id, consequat orci. Etiam rhoncus lacinia dignissim. Proin pretium nunc at nisl imperdiet, eget aliquet quam interdum. Proin sit amet porttitor libero. Nullam sit amet rhoncus sem. Morbi lobortis enim in mauris molestie vestibulum. Phasellus nec metus et dolor egestas ultrices. Vivamus in massa odio. Nullam ac erat at nisi faucibus maximus. Vivamus est purus, eleifend ornare eros quis, vulputate auctor nibh. Pellentesque vehicula lorem in ornare porta. Nam tristique, nisl sit amet porta pretium, nunc dui blandit nulla, fermentum efficitur neque lorem vel eros.'
        post5.tags = ['mongoengine', 'python']
        post5.save()

        return "Database initialized successfully :)."

    @app.route('/dummy/generate/posts/<int:number>')
    def generate_dummy_data(number):

        cookie = User.objects(username='cookie').get()

        for i in range(1, number + 1):
            post = TextPost(
                title=f"Dummy Post #{i}", author=cookie, published=True)
            post.published_at = datetime.now()
            post.content = 'Nulla venenatis, nisi et semper pharetra, augue orci consectetur enim, ullamcorper porta metus nunc nec risus. Vestibulum id lacus sed erat tempus elementum a et est. Nulla tincidunt molestie fermentum. Ut mattis diam nec augue volutpat, eu molestie libero bibendum. Sed tempus diam non interdum euismod. Aliquam aliquam maximus tincidunt. Ut suscipit, erat ut aliquam dignissim, augue nibh aliquam nunc, a porta tellus massa nec erat. Integer ultrices, leo ut feugiat maximus, ipsum erat porttitor est, nec mollis ipsum odio ac nisi. In suscipit leo eget facilisis malesuada. Cras mollis vitae odio at maximus. Nulla nunc libero, sodales quis purus a, lobortis dapibus felis. Donec aliquet varius sapien ut tristique. Sed eros turpis, sodales eget tristique non, consequat id mi. Vestibulum risus nisl, gravida eget convallis maximus, sagittis quis metus. Nam hendrerit elit tellus, non euismod nisl sagittis non. Curabitur pharetra massa nec tortor convallis hendrerit. Ut a sodales felis. Nullam euismod ipsum ac quam lacinia, nec elementum ex fringilla. Vestibulum et lectus libero. Aliquam non malesuada ante, venenatis imperdiet quam. Pellentesque auctor interdum justo, sit amet rutrum enim consequat sed. Suspendisse in est nibh. Pellentesque vitae mattis quam. Curabitur elementum volutpat sollicitudin. Sed eleifend sapien vitae felis interdum, at tincidunt nibh convallis. Pellentesque in ullamcorper lectus. Quisque bibendum rutrum lacus vel consequat. Curabitur lacinia ornare dignissim. Suspendisse pharetra vel lorem nec ultricies. Vivamus vitae tortor et ante posuere ornare. Curabitur mollis sapien vitae auctor accumsan. Nam venenatis neque eu malesuada sagittis. Suspendisse volutpat feugiat sapien. Sed convallis ex vel nibh blandit, vitae elementum eros imperdiet. Suspendisse blandit interdum justo, ac condimentum ipsum. Donec aliquam porta magna. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc elementum velit eu erat porttitor porttitor a ac dolor. In hac habitasse platea dictumst. Aenean ex velit, malesuada at venenatis nec, venenatis quis odio. Vestibulum pulvinar elementum rhoncus. Cras maximus dolor quam, eu venenatis velit dignissim vitae. Sed elit ex, pellentesque vitae euismod in, venenatis sed mauris. Donec porttitor semper pellentesque. Nunc condimentum magna urna, quis ultricies justo ullamcorper id. Donec facilisis et orci quis venenatis. Nulla id tempus libero. Praesent hendrerit euismod mattis. Donec convallis neque congue ante laoreet, at hendrerit dui euismod. Sed nec sollicitudin lorem. Praesent tincidunt justo eget nisi efficitur, eu semper urna feugiat. Nunc ipsum velit, pretium nec eleifend vitae, vestibulum eget mi. Suspendisse faucibus a felis in gravida. Maecenas fringilla lorem diam, in tempus nisl ultricies et. Sed elit mauris, hendrerit eu ullamcorper nec, auctor sed velit. In eget lectus pharetra, dignissim nisi id, consequat orci. Etiam rhoncus lacinia dignissim. Proin pretium nunc at nisl imperdiet, eget aliquet quam interdum. Proin sit amet porttitor libero. Nullam sit amet rhoncus sem. Morbi lobortis enim in mauris molestie vestibulum. Phasellus nec metus et dolor egestas ultrices. Vivamus in massa odio. Nullam ac erat at nisi faucibus maximus. Vivamus est purus, eleifend ornare eros quis, vulputate auctor nibh. Pellentesque vehicula lorem in ornare porta. Nam tristique, nisl sit amet porta pretium, nunc dui blandit nulla, fermentum efficitur neque lorem vel eros.'
            post.tags = ['mongoengine', 'python']
            post.save()

        return f"{number} posts generated."

    # register the 'post' blueprint
    from .blueprints.post import post_bp
    app.register_blueprint(post_bp)

    # register the 'user' blueprint
    from .blueprints.user import user_bp
    app.register_blueprint(user_bp)

    # register the 'login' blueprint
    from .blueprints.login import login_bp
    app.register_blueprint(login_bp)

    # register the 'search' blueprint
    from .blueprints.search import search_bp
    app.register_blueprint(search_bp)

    return app
