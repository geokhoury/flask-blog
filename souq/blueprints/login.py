from flask import Flask,Blueprint, render_template,request ,redirect,session,flash
from flask.helpers import url_for
from souq.forms import LoginForm
from souq.models import User
from flask_hashing import Hashing



# define our blueprint
login_bp = Blueprint('login', __name__)
app = Flask(__name__)
hashing = Hashing(app)

@login_bp.route('/login', methods =['POST','GET'])
def login():
    # create instance of our form
    login_form = LoginForm()
    # handle form submission
    if login_form.validate_on_submit():
        # read post values from the form
        username = login_form.username.data
        password = hashing.hash_value(login_form.password.data, salt='abcd')
        # get the DB connection
        # authenticate the user        
        # fetch user if the username exists in the DB
        user=User.objects(username=username).first()
        # print(str(user.id))
            # check if the user was found and the password matches
        if (user.username == username) and (user.password == password):
            session['user'] = user.serialize()
            # redirect the user after login
            return redirect(url_for('item.index'))
        else:
            # redirect to 404 if the login was invalid
            flash("Your Username or password is wrong please try again :( .")
            return render_template("login/login.html", form = login_form)
            # Render the login template
    return render_template("login/login.html", form = login_form)

@login_bp.route('/session')
def show_session():
    return dict(session)

@login_bp.route('/logout')
def logout():
    #Drop the user session :)
    session.clear()
    #redirect to root page 
    return redirect("/")