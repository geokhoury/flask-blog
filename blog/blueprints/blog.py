from flask import Blueprint, render_template,request ,session, redirect
from blog.db import get_db
import sqlite3
import datetime
from ..forms import AddPostForm

# define our blueprint
blog_bp = Blueprint('blog', __name__)



@blog_bp.route('/')
@blog_bp.route('/posts')
def index():
    # get the DB connection
    db = get_db()

    # retrieve all posts
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username,first_name,last_name'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    # render 'blog' blueprint with posts
    return render_template('blog/posts.html', posts=posts)

@blog_bp.route('/add/post', methods = ['GET', 'POST'])
def add_post():

    # create instance of our form
    add_post_form = AddPostForm()

    # handle form submission
    if add_post_form.validate_on_submit():
        # read post values from the form
        title = add_post_form.title.data
        body = add_post_form.body.data

        # read the 'uid' from the session for the current logged in user
        author_id = session['uid']

        # get the DB connection
        db = get_db()
        
        try:
            # insert post into database
            db.execute("INSERT INTO post (author_id, title, body) VALUES (?, ?,?);", (author_id,title, body))
            
            # commit changes to the database
            db.commit()
            
            return redirect('/posts')

        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            return redirect("/404")

    # render the template
    return render_template("blog/add-post.html",form=add_post_form)