from flask import Blueprint, render_template,request ,session, redirect,url_for,flash
from blog.db import get_db
import sqlite3
import datetime
from ..forms import AddPostForm,EditPostForm

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


@blog_bp.route('/delete/post/<int:post_id>')
def delete_post(post_id):

    # get the DB connection
    db = get_db()

    # update user information
    db.execute(f"""DELETE FROM post WHERE id = {post_id};""")
    db.commit()
    db = get_db()

    return redirect(url_for('blog.index'))


@blog_bp.route('/post/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    
    # create instance of our form
    edit_post_form = EditPostForm()
    
    if request.method == "GET":
        # get the DB connection
        db = get_db()

        # get user by id
        post = db.execute(f'''select body from post  WHERE id = {id}''').fetchone()

        edit_post_form.body.data = post['body']

    # handle form submission
    
    if edit_post_form.validate_on_submit():

        

        # read post values from the form
        body = edit_post_form.body.data

        print(body)
        # get the DB connection
        db = get_db()
        
        try:
            # update post information
            db.execute(f"""UPDATE post SET body = '{body}' WHERE id = '{id}'   """)
            db.commit()
            

            #  flash masseag
            flash("post information updated successfully!")

            # redirect  
            return redirect(url_for('blog.index'))

        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            return redirect("/404")

    # redner the login template
    return render_template("blog/edit-post.html", form = edit_post_form)
