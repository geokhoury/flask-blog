import sqlite3
from flask import Blueprint, render_template, request, redirect,session,flash
from blog.db import get_db
from ..forms import EditUserForm
from ..forms import EditPasswordForm

# define our blueprint
user_bp = Blueprint('user', __name__)


@user_bp.route('/add/user', methods=['GET', 'POST'])
def add_user():
    
    if request.method == 'GET':
        # render add user blueprint
        return render_template('user/add-user.html')
    else:
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        biography = request.form['biography']

        # get the DB connection
        db = get_db()

        # insert user into DB
        try:
            # execute our insert SQL statement
            db.execute("INSERT INTO user (username, first_name, last_name, biography, password) VALUES (?, ?, ?, ?, ?);", (username, first_name, last_name, biography, password))

            # write changes to DB
            db.commit()
            
            return redirect("/users")

        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            return redirect("/404")


@user_bp.route('/edit/user', methods=['GET', 'POST'])
def edit_user():
    
    # create instance of our form
    edit_user_form = EditUserForm()
    if request.method == "GET":
        edit_user_form.first_name.data = session['first_name']
        edit_user_form.last_name.data = session['last_name']
        edit_user_form.biography.data = session['biography']

    # handle form submission
    
    if edit_user_form.validate_on_submit():

        

        # read post values from the form
        first_name = edit_user_form.first_name.data
        last_name = edit_user_form.last_name.data
        biography = edit_user_form.biography.data

        print(first_name,last_name)
        # get the DB connection
        db = get_db()
        
        try:
            # update user information
            db.execute(f"""UPDATE user SET first_name = '{first_name}', last_name ='{last_name}',biography = '{biography}' WHERE id = '{session['uid']}'   """)
            db.commit()
            
            # update session
            session['first_name'] = first_name
            session['last_name'] = last_name
            session['biography'] = biography

        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            return redirect("/404")

    # redner the login template
    return render_template("user/edit-user.html", form = edit_user_form)


@user_bp.route('/edit/password', methods=['GET', 'POST'])
def edit_password():
    
    # create instance of our form
    edit_password_form = EditPasswordForm()
    
    
    if edit_password_form.validate_on_submit():

        

        # read post values from the form
        old_password = edit_password_form.old_password.data
        new_password = edit_password_form.new_password.data
        confirm = edit_password_form.confirm.data

       
        # get the DB connection
        db = get_db()
        
        try:
            
            # update user information
            db.execute(f"""UPDATE user SET password = '{confirm}' WHERE id = '{session['uid']}'   """)
            db.commit()
            flash('password changed')
            
            

        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            return redirect("/404")

    # redner the login template
    return render_template("user/edit-password.html", form = edit_password_form)



@user_bp.route('/users')
def get_users():
    # get the DB connection
    db = get_db()

    # get all users from the db
    users = db.execute('select * from user').fetchall()

    # render 'list.html' blueprint with users
    return render_template('user/list.html', users=users)


