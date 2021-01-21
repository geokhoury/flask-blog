from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired, InputRequired, EqualTo, Length


class AddPostForm(FlaskForm):
    title = StringField("Enter a title",validators=[ Length(min=10, max=20,message='at least 10 character for the title')],id='title')
    body = TextAreaField("Enter your text",validators=[Length(200,30000,'the body of post have to be at least 200 character')],default='6')
    submit = SubmitField("Add post")


class EditPostForm(FlaskForm):
    title = StringField("Enter a title")
    content = TextAreaField("Enter your content")
    submit = SubmitField("Edit post")


class AddCommentForm(FlaskForm):
    title = StringField("Enter a title")
    body = TextAreaField("Enter your text")
    submit = SubmitField("Add comment")
