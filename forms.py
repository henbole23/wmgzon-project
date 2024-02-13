from flask_wtf import FlaskForm
import wtforms as form
from wtforms.validators import ValidationError, DataRequired, InputRequired, Length
from wtforms.widgets import PasswordInput


class LoginForm(FlaskForm):
    username = form.StringField(label='username', validators=[DataRequired()])
    password = form.PasswordField(label='Password', validators=[DataRequired()])
    submit = form.SubmitField("Log In")


class RegisterForm(FlaskForm):
    email = form.StringField(label='Email Address', validators=[DataRequired()])
    username = form.StringField(label='username', validators=[DataRequired()])
    password = form.PasswordField(label='Password', validators=[DataRequired()])
    submit = form.SubmitField("Register")

class AdminAlbumForm(FlaskForm):
    name = form.StringField(label='Album Name', validators=[DataRequired()])
    artwork = form.StringField(label='Album Artwork', validators=[DataRequired()])
    collection_type = form.RadioField(label='Collection Type', choices=[('LP', 'LP'), ('EP', 'EP'), ('Single', 'Single')], validators=[InputRequired()])
    genre = form.StringField(label='Genre', validators=[DataRequired()])
    year = form.IntegerField(label="Release Year", validators=[DataRequired()])

