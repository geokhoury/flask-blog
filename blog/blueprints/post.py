from flask import Blueprint, render_template, request, session, redirect, url_for
import datetime
from bson import ObjectId

from blog.models import TextPost
from blog.forms import AddPostForm, EditPostForm

# define our blueprint
post_bp = Blueprint('post', __name__)


@post_bp.route('/')
@post_bp.route('/posts/new')
def index():
    # get all newly published posts
    new_posts = TextPost.objects.get_new_posts()

    # render 'blog' blueprint with posts
    return render_template('post/posts.html', posts=new_posts, title='New Posts', icon="fas fa-asterisk")


@post_bp.route('/posts/trending')
def trending():
    # get all trending posts
    trending_posts = TextPost.objects.get_trending_posts()

    # render 'blog' blueprint with posts
    return render_template('post/posts.html', posts=trending_posts, title='Trending Posts', icon="fas fa-chart-line")


@post_bp.route('/posts/me')
def user_posts():
    # get all posts
    user_posts = TextPost.objects.get_published_by_user()

    # render 'blog' blueprint with posts
    return render_template('post/posts.html', posts=user_posts, title='Posts by You', icon="fas fa-feather-alt")


@post_bp.route('/posts/drafts')
def user_drafts():
    # get all posts
    user_drafts = TextPost.objects.get_user_drafts()

    # render 'blog' blueprint with posts
    return render_template('post/posts.html', posts=user_drafts, title='Your Drafts', icon="fab fa-firstdraft")


@post_bp.route('/post/add', methods=['GET', 'POST'])
def add_post():

    # create instance of our form
    add_post_form = AddPostForm()

    # handle form submission
    if add_post_form.validate_on_submit():

        # read post values from the form
        title = add_post_form.title.data
        content = add_post_form.content.data

        # create instance of TextPost
        post = TextPost(title=title, content=content)
        post.author = ObjectId(session['user']['id'])
        post.tags = ["flask", "python", "mongo"]

        # check if post is being published then change the published attribute
        if add_post_form.publish.data:
            post.published = True
            post.save()
            # redirect to user_published
            return redirect(url_for('post.user_posts'))            
        
        post.save()

        # redirect to user_drafts
        return redirect(url_for('post.user_drafts'))

    # render the template
    return render_template("post/add-post.html", form=add_post_form)


@post_bp.route('/post/<post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):

    # Find our post
    post = TextPost.objects(id=post_id).first()

    # create instance of our form
    edit_post_form = EditPostForm()

    if request.method == 'GET':
        edit_post_form.title.data = post.title
        edit_post_form.content.data = post.content

    # handle form submission
    if edit_post_form.validate_on_submit():

        # read post values from the form
        title = edit_post_form.title.data
        content = edit_post_form.content.data

        # Update our post title and content
        post.title = title
        post.content = content

        # save our changes to the DB
        post.save()

        # render the template
        return redirect(url_for('post.index'))

    # render the template
    return render_template("post/edit-post.html", form=edit_post_form)


@post_bp.route('/post/<post_id>')
def view_post(post_id):

    # get post
    post = TextPost.objects(id=post_id).first()
    if post.published:
        TextPost.objects(id=post_id).update_one(inc__view_count=1)
        post.reload()

    # render the view
    return render_template('post/view-post.html', post=post)


@post_bp.route('/post/<post_id>/publish')
def publish_post(post_id):

    # get post
    post = TextPost.objects(id=post_id).get()

    if post.author.id == ObjectId(session['user']['id']):
        post.publish()

    # render the view
    return redirect(url_for('post.user_posts'))


@ post_bp.route('/post/<post_id>/delete')
def delete_post(post_id):

    # get post
    TextPost.objects(id=post_id).first().delete()

    # render the view
    return redirect(url_for('post.index'))
