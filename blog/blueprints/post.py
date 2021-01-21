from blog.models.post import Post
from itertools import count
from flask import Blueprint, render_template, request, session, redirect, url_for
import datetime
from blog.models import User, comment
from blog.models import Comment

from blog.models import TextPost
from blog.forms import AddPostForm, EditPostForm , AddCommentForm

# define our blueprint
post_bp = Blueprint('post', __name__)


@post_bp.route('/')
@post_bp.route('/posts')
def index():
    # get all posts
    posts = TextPost.objects()
    

    # render 'blog' blueprint with posts
    return render_template('post/posts.html', posts=posts)


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
        post.author =  User.get_by_username(User,session['username'])
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


@post_bp.route('/post/<post_id>',methods=['POST','GET'])
def view_post(post_id):
    post = TextPost.objects(id=post_id).first()
    # create instance of our form
    add_comment_form = AddCommentForm()
    # handle form submission
    if add_comment_form.validate_on_submit():
        # read post values from the form
        title = add_comment_form.title.data
        body = add_comment_form.body.data
        user = User.objects(id=session['uid']).first()
        # create instance of TextPost
        comment = Comment(content=body,author=user)
        # add comment to post comments
        post.comments.append(comment)
        post.save()
        
        return render_template('post/view.html', post=post ,form=add_comment_form)
        

    # get post


    # render the view
    return render_template('post/view.html', post=post,form=add_comment_form)


@post_bp.route('/post/delete/<post_id>')
def delete_post(post_id):

    # get post
    TextPost.objects(id=post_id).first().delete()

    # render the view
    return redirect(url_for('post.index'))

@post_bp.route('/delete-comment/<post_id>/<content>')
def delete_comment(post_id,content):
    # get post
    post = Post.objects(id=post_id).first()
    #get a comment of post
    post.comments
    count=0
    for i in post.comments:
        if i.content == content:
            post.comments.pop(count)
            post.save()
            break
        count+=1    
    # render the view
    return redirect(url_for('post.index'))


@post_bp.route('/trending')
def trending():
    # get all posts
    posts = TextPost.objects.order_by('-created_at')
    # render 'blog' blueprint with posts
    return render_template('post/posts.html', posts=posts, title='Trending Posts')
