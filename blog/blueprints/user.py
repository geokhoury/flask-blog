from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from flask_pymongo import PyMongo 
from blog.models import User
# from blog.models import TextUser
from blog.forms import EditUserForm, AddUserForm

# define our blueprint
user_bp = Blueprint('user', __name__)


@user_bp.route('/add/user', methods=['GET', 'POST'])
def add_user():

    # create instance of our form
    add_user_form = AddUserForm()

    # handle form submission
    if add_user_form.validate_on_submit():

        # create user object
        user = User()

        # set object attributes
        user.username = add_user_form.username.data
        user.password = add_user_form.password.data
        user.first_name = add_user_form.first_name.data
        user.last_name = add_user_form.last_name.data
        user.biography = add_user_form.biography.data

        # save the user object
        user.save()
        return redirect(url_for('post.index'))
    else:
        return render_template("user/add-user.html", form=add_user_form)

        # # another way
        # my_user = User(username = 'cookie', password = '1234')
        # my_user.save()

    # render the template
   


@user_bp.route('/user/edit/<id>', methods=['GET', 'POST'])
def edit_user(id):
    user = User.objects(id=id).first()

    # create instance of our form
    edit_user_form = EditUserForm()
    if request.method == "GET":
        edit_user_form.first_name.data = user.first_name
        edit_user_form.last_name.data = user.last_name
        edit_user_form.biography.data = user.biography

    # handle form submission

    if edit_user_form.validate_on_submit():

        # read post values from the form
        first_name = edit_user_form.first_name.data
        last_name = edit_user_form.last_name.data
        biography = edit_user_form.biography.data

        # Update our user data

        user.first_name=first_name
        user.last_name=last_name
        user.biography=biography

        # save our changes to the DB
        user.save()

         # render the template
        return redirect(url_for('user.view_user', id=session['uid']))


    # redner the login template
    return render_template("user/edit-user.html", form=edit_user_form)


@user_bp.route('/users')
def get_users():

    # get all users
    users = User.objects

    # render 'list.html' blueprint with users
    return render_template('user/list.html', users=users)


@user_bp.route('/user/view/<id>')
def view_user(id):

    # get user by id
    user = User.objects(id=id).first()
    # render 'profile.html' blueprint with user
    return render_template('user/view-user.html', user=user)


@user_bp.route('/user/delete/<id>')
def delete_user(id):

    # get user by id
    User.objects(id=id).first().delete()
    session.clear()

    # render 'profile.html' blueprint with user
    return redirect(url_for('login.logout'))