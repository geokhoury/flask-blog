from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import InputRequired, EqualTo


class AddPostForm(FlaskForm):
    title = StringField("Title", render_kw={"placeholder":"Why I love Flask?"})
    content = TextAreaField("Content", render_kw={"placeholder":"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Etiam non quam lacus suspendisse faucibus interdum posuere lorem ipsum. Eu augue ut lectus arcu. Velit euismod in pellentesque massa placerat duis ultricies lacus sed. Cursus metus aliquam eleifend mi in nulla. Auctor elit sed vulputate mi sit amet mauris commodo quis. Ac tincidunt vitae semper quis lectus nulla at volutpat. Fames ac turpis egestas integer eget aliquet nibh praesent."})
    publish = SubmitField("Publish Post")
    save_draft = SubmitField("Save as Draft")


class EditPostForm(FlaskForm):
    title = StringField("Title")
    content = TextAreaField("Content")
    update = SubmitField("Update post")
