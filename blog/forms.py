from flask_wtf import FlaskForm 
from wtforms import StringField,TextAreaField,SubmitField,PasswordField

class AddPostForm(FlaskForm):
    title=StringField("Enter a title")
    body=TextAreaField("Enter your text")
    submit=SubmitField("Add post")

class LoginForm(FlaskForm):
    username=StringField("Enter your username")
    password=PasswordField("Enter your password")
    submit=SubmitField("Login")

    

