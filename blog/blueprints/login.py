from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from blog.forms import LoginForm
from blog.models import User

# define our blueprint
login_bp = Blueprint('login', __name__)


@login_bp.route('/login', methods=['POST', 'GET'])
def login():
    # create instance of our form
    login_form = LoginForm()

    # handle form submission
    if login_form.validate_on_submit():

        # read post values from the form
        username = login_form.username.data
        password = login_form.password.data

        # get the user object
        user = User.objects(username=username).first()

        # check if the user was found and the password matches
        if (user) and (user.authenticate(username, password)):
            session['user'] = user.serialize()
            # redirect the user after login
            print(">>",request.args['next'])
            return redirect(request.args['next'])
        else:
            # invalid credentials, redirect to login with error message
            flash("Login invalid. Please check your username and password.")
            return redirect(url_for('login.login'))

    # render the login template
    return render_template("login/login.html", form=login_form)


@login_bp.route('/session')
def show_session():
    return dict(session)


@login_bp.route('/logout')
def logout():
    # clear user session
    session.clear()

    # redirect to index
    return redirect(url_for('post.index'))
