from flask_wtf import FlaskForm 
from wtforms import StringField,TextAreaField,SubmitField,PasswordField
from wtforms.validators import InputRequired,EqualTo

class LoginForm(FlaskForm):
    username=StringField("Username", validators=[InputRequired()], render_kw={"placeholder": "bert"})
    password=PasswordField("Password", validators=[InputRequired()], render_kw={"placeholder": "secret123"})
    submit=SubmitField("Login")

