from flask_wtf import FlaskForm
from mongoengine.fields import DateField, DateTimeField
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField,DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo
import email_validator


class EditUserForm(FlaskForm):
    username=StringField("Enter your username",validators=[ Length(min=2, max=20),DataRequired()])
    email= StringField("Email",validators=[DataRequired(),Email('Please enter your email correctly')])
    birthday = DateField('Date of birth', validators=[DataRequired()], format='%Y-%m-%d') 
    # Secondary 
    first_name = StringField("Enter your first name",validators=[DataRequired(),Length(min=2, max=20)])
    last_name = StringField("Enter your last name",validators=[DataRequired(),Length(min=2, max=20)])
    biography = TextAreaField("Enter your biography",validators=[DataRequired(),Length(min=50, max=250)])
    submit=SubmitField("Add User")

class Registerion(FlaskForm):
    # Data of new user
    username=StringField("Enter your username",validators=[ Length(min=2, max=20),DataRequired()])
    email= StringField("Email",validators=[DataRequired(),Email('Please enter your email correctly')])
    birthday = DateField('Date of birth', validators=[DataRequired()], format='%Y-%m-%d') 
    # Password
    password= PasswordField('Password', [DataRequired()])
    confirm_password=PasswordField('Confirm Password',validators=[ DataRequired(), EqualTo('password',message="Password miss match")])
    # Secondary 
    first_name = StringField("Enter your first name",validators=[DataRequired(),Length(min=2, max=20)])
    last_name = StringField("Enter your last name",validators=[DataRequired(),Length(min=2, max=20)])
    biography = TextAreaField("Enter your biography",validators=[DataRequired(),Length(min=50, max=250)])
    submit=SubmitField("Add User")



# Change Password Form
class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(
        'Enter your current password', [DataRequired()])
    new_password = PasswordField('Enter your new password', [DataRequired(), EqualTo('confirm_password')])
    confirm_password = PasswordField(
        "Confirm your new password", [DataRequired()])
    change_password = SubmitField("Change password")