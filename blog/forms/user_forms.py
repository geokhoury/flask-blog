from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class EditUserForm(FlaskForm):
    first_name = StringField("Enter your first name")
    last_name = StringField("Enter your last name")
    biography = TextAreaField("Enter your biography")
    submit=SubmitField("Update User")

class AddUserForm(FlaskForm):
    username=StringField("Enter your username",validators=[ Length(min=2, max=20),DataRequired()])
    password= PasswordField('Password', [DataRequired()])
    confirm_password=PasswordField('Confirm Password',validators=[ DataRequired(), EqualTo('password',message="password miss match")])
    first_name = StringField("Enter your first name")
    last_name = StringField("Enter your last name")
    biography = TextAreaField("Enter your biography")
    submit=SubmitField("Add User")