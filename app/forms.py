from flask_wtf import FlaskForm
import wtforms as form
from wtforms.validators import InputRequired, DataRequired, Length
import datetime

class LoginForm(FlaskForm):
    username = form.StringField(label='username', validators=[InputRequired(message="Input Required")])
    password = form.PasswordField(label='Password', validators=[InputRequired(message="Input Required")])
    submit = form.SubmitField("Log In")


class RegisterForm(FlaskForm):
    email = form.EmailField(label='Email Address', validators=[InputRequired(message="Input Required")])
    username = form.StringField(label='username', validators=[InputRequired(message="Input Required")])
    password = form.PasswordField(label='Password', validators=[InputRequired(message="Input Required")])
    submit = form.SubmitField("Register")

class AdminAlbumForm(FlaskForm):
    album_name = form.StringField(label='Album Name', validators=[InputRequired(message="Input Required")])
    artwork = form.StringField(label='Album Artwork', validators=[InputRequired(message="Input Required")])
    genre = form.SelectField(label='Genre')
    new_genre = form.StringField(label='New Genre')
    year = form.IntegerField(label="Release Year", validators=[InputRequired(message="Input Required")])
    artist_name = form.SelectField(label='Artist Name')
    new_artist_name = form.StringField(label='New Artist Name')
    submit = form.SubmitField("Submit")

class AdminArtistForm(FlaskForm):
    artist_name = form.StringField(label='Artist Name', validators=[InputRequired(message="Input Required")])
    artist_bio = form.StringField(label='Artist Bio')
    submit = form.SubmitField("Submit")

class AdminGenreForm(FlaskForm):
    genre = form.StringField(label='Genre Name', validators=[InputRequired(message="Input Required")])
    submit = form.SubmitField("Submit")

class ProductForm(FlaskForm):
    product_id = form.IntegerField(label='ID')
    name = form.StringField(label='Name')
    image = form.StringField(label='Image File (include file format)')
    price = form.DecimalField(label='Price', places=2)
    type = form.StringField(label='Type') 
    submit = form.SubmitField("Submit")

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
    
