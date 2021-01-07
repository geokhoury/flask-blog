import sqlite3
from flask import Blueprint, render_template, request, redirect,session,flash,url_for
from blog.db import get_db
from ..forms import EditUserForm,AddUserForm


# define our blueprint
user_bp = Blueprint('user', __name__)


@user_bp.route('/add/user', methods=['GET', 'POST'])
def add_user():

    # create instance of our form
    add_user_form = AddUserForm()

    # handle form submission
    if add_user_form.validate_on_submit():
        # read post values from the form
        username = add_user_form.username.data
        password = add_user_form.password.data
        first_name = add_user_form.first_name.data
        last_name = add_user_form.last_name.data
        biography = add_user_form.biography.data


        # get the DB connection
        db = get_db()
        
        try:
            # insert post into database
            db.execute("INSERT INTO user (username, password, first_name, last_name,biography) VALUES (?, ?,?,?,?);", (username, password, first_name, last_name,biography))
            
            # commit changes to the database
            db.commit()
            
            # flash sin up masseag to user
            flash("Account successfully created! Please log in.")

            return redirect('/login')

        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            return redirect("/404")

    # render the template
    return render_template("user/add-user.html",form=add_user_form)

@user_bp.route('/user/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    
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

            #  flash masseag
            flash("User information updated successfully!")

            # redirect  
            return redirect(url_for('user.view_user',id=session['uid']))

        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            return redirect("/404")

    # redner the login template
    return render_template("user/edit-user.html", form = edit_user_form)


@user_bp.route('/users')
def get_users():
    # get the DB connection
    db = get_db()

    # get all users from the db
    users = db.execute('select * from user').fetchall()

    # render 'list.html' blueprint with users
    return render_template('user/list.html', users=users)

@user_bp.route('/user/view/<int:id>')
def view_user(id):
    # get the DB connection
    db = get_db()

    # get user by id
    user = db.execute(f'''select * from user  WHERE id = {id}''').fetchone()

    # render 'profile.html' blueprint with user
    return render_template('user/view-user.html', user=user)




