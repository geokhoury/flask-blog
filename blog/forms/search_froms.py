from flask_wtf import FlaskForm 
from wtforms import StringField,TextAreaField,SubmitField,PasswordField
from wtforms.validators import InputRequired,EqualTo

class TextSearchForm(FlaskForm):
    keyword=StringField("keyword", validators=[InputRequired()], render_kw={"placeholder": "What are you looking for?"})
    search=SubmitField("Search")

