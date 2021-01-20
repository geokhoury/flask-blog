from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import InputRequired, EqualTo


class AddPostForm(FlaskForm):
    title = StringField("Enter a title")
    body = TextAreaField("Enter your text")
    submit = SubmitField("Add post")
    save_at_draft=SubmitField("Save As Draft")


class EditPostForm(FlaskForm):
    title = StringField("Enter a title")
    content = TextAreaField("Enter your content")
    submit = SubmitField("Edit post")

class DraftPostForm(FlaskForm):
    submit = SubmitField("Draft")
