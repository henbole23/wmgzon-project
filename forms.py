from flask_wtf import FlaskForm
import wtforms as form
from wtforms.validators import InputRequired, DataRequired, Length
import datetime

class LoginForm(FlaskForm):
    username = form.StringField(label='username', validators=[InputRequired(message='Input Required')])
    password = form.PasswordField(label='Password', validators=[InputRequired(message='Input Required')])
    submit = form.SubmitField('Log In')

class RegisterForm(FlaskForm):
    email = form.EmailField(label='Email Address', validators=[InputRequired(message='Input Required')])
    username = form.StringField(label='username', validators=[InputRequired(message='Input Required')])
    password = form.PasswordField(label='Password', validators=[InputRequired(message='Input Required')])
    submit = form.SubmitField('Register')
    
class UserEditForm(FlaskForm):
    username = form.StringField(label='Username')
    email = form.EmailField(label='Email')
    type = form.SelectField(label='Role', choices=[('Admin', 'Admin'), ('Customer', 'Customer')])
    submit = form.SubmitField(label='Edit')
    

class AlbumForm(FlaskForm):
    album_id = form.IntegerField(label='ID')
    album_name = form.StringField(label='Album Name')
    year = form.IntegerField(label='Release Year')
    fk_artist_id = form.IntegerField(label='Artist ID')
    fk_product_id = form.IntegerField(label='Product ID')
    submit = form.SubmitField('Submit')
    
class SongForm(FlaskForm):
    name = form.StringField(label='Song Name')
    length = form.IntegerField(label='Length')
    submit = form.SubmitField('Add')

class ProductForm(FlaskForm):
    product_id = form.IntegerField(label='ID')
    product_name = form.StringField(label='Name')
    image = form.StringField(label='Image File (include file format)')
    price = form.DecimalField(label='Price', places=2)
    type = form.StringField(label='Type')
    stock = form.IntegerField(label='Stock Count')
    submit = form.SubmitField('Submit')
    
class MusicProductForm(ProductForm):
    album_name = form.StringField(label='Album Name')
    year = form.IntegerField(label='Release Year')
    artist_name = form.StringField(label='Artist Name')
    artist_bio = form.StringField(label='Artist Bio (Optional)')
    genres = form.SelectMultipleField(label='Genres', option_widget=form.widgets.CheckboxInput(), widget=form.widgets.ListWidget(prefix_label=False))


class AddressForm(FlaskForm):
    house_number = form.IntegerField(label='House/Flat Number')
    street = form.StringField(label='Street')
    city = form.StringField(label='City/Town')
    county = form.StringField(label='County')
    post_code = form.StringField(label='Post Code')

class PaymentForm(FlaskForm):
    card_number = form.StringField('Card Number', validators=[DataRequired(), Length(min=16, max=16)])
    expiration_month = form.SelectField('Expiration Date', choices=[(str(i), str(i)) for i in range(1, 13)], coerce=int, validators=[DataRequired()])
    expiration_year = form.SelectField('Expiration Date', choices=[(str(i), str(i)) for i in range(datetime.datetime.now().year, (datetime.datetime.now().year) + 10)], coerce=int, validators=[DataRequired()])
    cvv = form.StringField('CVV', validators=[DataRequired(), Length(min=3, max=4)])

class CheckoutForm(AddressForm, PaymentForm):
    email = form.EmailField(label='Email')
    submit = form.SubmitField(label='Submit Order')
    
class SearchForm(FlaskForm):
    search_field = form.StringField(label='Search Field', validators=[DataRequired()])
    submit = form.SubmitField(label='Search')
    
class FilterForm(FlaskForm):
    artist = form.SelectField(label='Artist')
    genre = form.SelectField(label='Genre')
    submit = form.SubmitField(label='Apply')
    
class SortForm(FlaskForm):
    year = form.SelectField(label='Year', choices=[('descend', 'Release Year: Newest to Oldest'), ('ascend', 'Release Year: Oldest to Newest')])
    submit = form.SubmitField(label='Submit')
