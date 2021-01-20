from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import InputRequired, EqualTo, Length


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(
        'Enter your current password', [InputRequired()])
    new_password = PasswordField('Enter your new password', [InputRequired(), EqualTo('confirm_password')])
    confirm_password = PasswordField(
        "Confirm your new password", [InputRequired()])
    change_password = SubmitField("Change password")


class EditUserForm(FlaskForm):
    first_name = StringField("Enter your first name")
    last_name = StringField("Enter your last name")
    biography = TextAreaField("Enter your biography")
    submit = SubmitField("Update User")


class AddUserForm(FlaskForm):
    username = StringField("Choose a username", validators=[
                           InputRequired(), Length(3, 20)])
    password = PasswordField('Enter a secure password', [InputRequired(), EqualTo(
        'confirm_password', message='Passwords must match')])
    confirm_password = PasswordField("Confirm your password")

    first_name = StringField("What is your first name?")
    last_name = StringField("What is your last name?")
    biography = TextAreaField("Enter your biography")
    submit = SubmitField("Create account")
