from flask import Blueprint, render_template,request ,redirect,session
from blog.forms import LoginForm
from blog.models import User


# define our blueprint
login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods =['POST','GET'])
def login():
    # create instance of our form
    login_form = LoginForm()
    # handle form submission
    if login_form.validate_on_submit():
        # read post values from the form
        username = login_form.username.data
        password = login_form.password.data
        # get the DB connection
        # authenticate the user        
        # fetch user if the username exists in the DB
        user=User.objects(username=username).first()
        # print(str(user.id))
            # check if the user was found and the password matches
        if (user.username==username) and (user.password==password):
            session['uid'] = str(user.id)
            session['username']=user.username
            session['first_name'] =user.first_name
            session['last_name'] =user.last_name
            session['biography'] =user.biography

        
                

            # redirect the user after login
            return redirect("/posts")
        else:
            # redirect to 404 if the login was invalid
            return redirect("/404")
    # redner the login template
    return render_template("login/login.html", form = login_form)

@login_bp.route('/session')
def show_session():
    return dict(session)

@login_bp.route('/logout')
def logout():
    # pop 'uid' from session
    session.clear()
    # redirect to index
    return redirect("/")