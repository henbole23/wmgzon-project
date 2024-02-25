from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, IntegerField, DecimalField, SelectMultipleField, SelectField, widgets, validators
import datetime


class LoginForm(FlaskForm):
    """Class for login form fields"""

    username = StringField(label='Username', validators=[
                           validators.InputRequired(), validators.Length(min=4, max=16)])
    password = PasswordField(label='Password', validators=[
                             validators.InputRequired(), validators.Length(min=8, max=16)])
    submit = SubmitField('Log In')


class RegisterForm(FlaskForm):
    """Class for register form fields"""

    email = EmailField(label='Email Address', validators=[
                       validators.InputRequired()])
    username = StringField(label='username', validators=[
                           validators.InputRequired(), validators.Length(min=3, max=16)])
    password = PasswordField(label='Password', validators=[validators.InputRequired(), validators.Length(
        min=8, max=16),  validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField(label='Confirm Password', validators=[
                            validators.InputRequired(), validators.Length(min=8, max=16)])
    submit = SubmitField('Register')


class UserEditForm(FlaskForm):
    """Class for editing user form fields"""

    username = StringField(label='Username')
    email = EmailField(label='Email')
    type = SelectField(label='Role', choices=[
                       ('Admin', 'Admin'), ('Customer', 'Customer')])
    submit = SubmitField(label='Edit')


class SongForm(FlaskForm):
    """Class for song form fields"""

    song_id = IntegerField(label='Song ID')
    name = StringField(label='Song Name')
    length = IntegerField(label='Length')
    submit = SubmitField('Add')


class ProductForm(FlaskForm):
    """Class for product form fields"""

    product_id = IntegerField(label='ID')
    name = StringField(label='Name')
    image = StringField(label='Image File (include file format)')
    price = DecimalField(label='Price', places=2)
    type = StringField(label='Type')
    stock = IntegerField(label='Stock Count')
    submit = SubmitField('Submit')


class MusicProductForm(ProductForm):
    """Class for music related product data form fields"""

    album_name = StringField(label='Album Name')
    year = IntegerField(label='Release Year')
    artist_name = StringField(label='Artist Name')
    artist_bio = StringField(label='Artist Bio (Optional)')
    genres = SelectMultipleField(label='Genres', option_widget=widgets.CheckboxInput(
    ), widget=widgets.ListWidget(prefix_label=False))


class AddressForm(FlaskForm):
    """Class for address form fields"""

    house_number = IntegerField(label='House/Flat Number')
    street = StringField(label='Street')
    city = StringField(label='City/Town')
    county = StringField(label='County')
    post_code = StringField(label='Post Code')


class PaymentForm(FlaskForm):
    """Class for payment form fields"""

    card_number = StringField('Card Number', validators=[
                              validators.InputRequired(), validators.Length(min=16, max=16)])
    expiration_month = SelectField('Expiration Date', choices=[(str(i), str(
        i)) for i in range(1, 13)], coerce=int, validators=[validators.InputRequired()])
    expiration_year = SelectField('Expiration Date', choices=[(str(i), str(i)) for i in range(datetime.datetime.now(
    ).year, (datetime.datetime.now().year) + 10)], coerce=int, validators=[validators.InputRequired()])
    cvv = StringField('CVV', validators=[
                      validators.InputRequired(), validators.Length(min=3, max=4)])


class CheckoutForm(AddressForm, PaymentForm):
    """Class for checkout form fields, inherits from AddressForm and PaymentForm"""

    email = EmailField(label='Email')
    submit = SubmitField(label='Submit Order')


class SearchForm(FlaskForm):
    """Class for search form fields"""

    search_field = StringField(label='Search Field', validators=[
                               validators.InputRequired()])
    submit = SubmitField(label='Search')


class FilterForm(FlaskForm):
    """Class for filter form fields"""

    artist = SelectField(label='Artist')
    genre = SelectField(label='Genre')
    submit = SubmitField(label='Apply')
