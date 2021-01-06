from flask_wtf import FlaskForm 
from wtforms import StringField,TextAreaField,SubmitField,PasswordField,validators

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

class EditPasswordForm(FlaskForm):
    old_password=PasswordField("Enter your old password")
    new_password=PasswordField('New Password', [validators.DataRequired(),validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    submit=SubmitField("update password")
   
   