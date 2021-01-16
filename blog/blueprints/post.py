from flask import Blueprint, render_template, request, session, redirect, url_for
import datetime
from blog.models import User
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
        
        return render_template('post/view-post.html', post=post ,form=add_comment_form)
        

    # get post


    # render the view
    return render_template('post/view-post.html', post=post,form=add_comment_form)


@post_bp.route('/post/delete/<post_id>')
def delete_post(post_id):

    # get post
    TextPost.objects(id=post_id).first().delete()

    # render the view
    return redirect(url_for('post.index'))

# @post_bp.route('/comment/add', methods=['GET', 'POST'])
# def add_comment():

#     # create instance of our form
#     add_comment_form = AddCommentForm()

#     # handle form submission
#     if add_comment_form.validate_on_submit():

#         # read post values from the form
#         title = add_comment_form.title.data
#         body = add_comment_form.body.data
#         user = User.objects(id=session['uid']).first()
    

#         # create instance of TextPost
#         comment = Comment(content=body,author=user)
#         post= TextPost(title=title,author=user,comments=[comment])
        
#         post.save()

#         # render the template
#         return redirect(url_for('post.index'))

#     # render the template
#     return render_template("post/add-comment.html", form=add_comment_form)

# c1 = Comment(content='test comment 1',author=bert)
#         c2 = Comment(content='test comment 2',author=cookie)

#         # Create TextPost
#         post1 = TextPost(title='Fun with MongoEngine', author=bert,comments= [c1,c2])
