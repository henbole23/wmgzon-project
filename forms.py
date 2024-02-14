from flask_wtf import FlaskForm
import wtforms as form
from wtforms.validators import InputRequired


class LoginForm(FlaskForm):
    username = form.StringField(label='username', validators=[InputRequired(message="Input Required")])
    password = form.PasswordField(label='Password', validators=[InputRequired(message="Input Required")])
    submit = form.SubmitField("Log In")


class RegisterForm(FlaskForm):
    email = form.StringField(label='Email Address', validators=[InputRequired(message="Input Required")])
    username = form.StringField(label='username', validators=[InputRequired(message="Input Required")])
    password = form.PasswordField(label='Password', validators=[InputRequired(message="Input Required")])
    submit = form.SubmitField("Register")

class AdminAlbumForm(FlaskForm):
    album_name = form.StringField(label='Album Name', validators=[InputRequired(message="Input Required")])
    artwork = form.StringField(label='Album Artwork', validators=[InputRequired(message="Input Required")])
    collection_type = form.RadioField(label='Collection Type', choices=[('LP', 'LP'), ('EP', 'EP'), ('Single', 'Single')], validators=[InputRequired(message="Input Required")])
    genre = form.SelectField(label='Genre', validators=[InputRequired(message="Input Required")])
    year = form.IntegerField(label="Release Year", validators=[InputRequired(message="Input Required")])
    artist_name = form.SelectField(label='Artist Name')
    new_artist_name = form.StringField(label='New Artist Name')
    artist_bio = form.StringField(label='Artist Bio')
    submit = form.SubmitField("Add")

