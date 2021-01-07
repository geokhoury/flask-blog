from flask_wtf import FlaskForm 
from wtforms import StringField,TextAreaField,SubmitField,PasswordField
from wtforms.validators import InputRequired,EqualTo

class AddPostForm(FlaskForm):
    title=StringField("Enter a title")
    body=TextAreaField("Enter your text")
    submit=SubmitField("Add post")

class LoginForm(FlaskForm):
    username=StringField("Enter your username")
    password=PasswordField("Enter your password")
    submit=SubmitField("Login")

class EditUserForm(FlaskForm):
    first_name = StringField("Enter your first name")
    last_name = StringField("Enter your last name")
    biography = TextAreaField("Enter your biography")
    submit=SubmitField("Update User")

class AddUserForm(FlaskForm):
    username=StringField("Enter your username")
    password= PasswordField('New Password', [InputRequired(), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password=PasswordField("Repeat Password")

    first_name = StringField("Enter your first name")
    last_name = StringField("Enter your last name")
    biography = TextAreaField("Enter your biography")
    submit=SubmitField("Add User")



