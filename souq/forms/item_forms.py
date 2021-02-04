from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField,DecimalField ,IntegerField,FloatField
from wtforms.validators import DataRequired, InputRequired, EqualTo, Length


class AddItemForm(FlaskForm):
    title = StringField("Product name: ",validators=[ Length(min=10, max=20,message='at least 10 character for the title')],id='title')
    body = TextAreaField("Description: ",validators=[Length(200,30000,'the body of Item have to be at least 200 character')],default='Enter your product description')
    price = FloatField("Enter the price: ", validators=[DataRequired()])
    quantity = IntegerField("Enter the quantity: ", validators=[DataRequired()])
    selling_price = FloatField("Enter the selling price: ",validators=[DataRequired()])
    submit = SubmitField("Add Item")


class EditItemForm(FlaskForm):
    title = StringField("Enter a title")
    content = TextAreaField("Enter your content")
    submit = SubmitField("Edit Item")


class AddCommentForm(FlaskForm):
    title = StringField("Enter a title: ")
    body = TextAreaField("Enter your Product Description: ")
    submit = SubmitField("Add comment: ")


class AddCard(FlaskForm):
    user_id = StringField()
    items = StringField()
