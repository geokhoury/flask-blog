from flask import Blueprint, render_template, request, session, redirect, url_for
import datetime

from blog.models import TextPost
from blog.forms import AddPostForm, EditPostForm

# define our blueprint
post_bp = Blueprint('post', __name__)


@post_bp.route('/')
@post_bp.route('/new')
def index():
    # get all posts
    posts = TextPost.objects

    # render 'blog' blueprint with posts
    return render_template('post/posts.html', posts=posts, title = 'New Posts')

@post_bp.route('/trending')
def trending():
    # get all posts
    posts = TextPost.objects

    # render 'blog' blueprint with posts
    return render_template('post/posts.html', posts=posts, title = 'Trending Posts')



@post_bp.route('/post/add', methods=['GET', 'POST'])
def add_post():

    # create instance of our form
    add_post_form = AddPostForm()

    # handle form submission
    if add_post_form.validate_on_submit():

        # read post values from the form
        title = add_post_form.title.data
        content = add_post_form.body.data

        # create instance of TextPost
        post = TextPost(title=title, content=content)
        post.tags = ["flask", "python", "mongo"]
        post.save()

        # render the template
        return redirect(url_for('post.index'))

    # render the template
    return render_template("post/add-post.html", form=add_post_form)


@post_bp.route('/post/edit/<post_id>', methods=['GET', 'POST'])
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

    # render the view
    return render_template('post/view-post.html', post=post)


@post_bp.route('/post/delete/<post_id>')
def delete_post(post_id):

    # get post
    TextPost.objects(id=post_id).first().delete()

    # render the view
    return redirect(url_for('post.index'))
