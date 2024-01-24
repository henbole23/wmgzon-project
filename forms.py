from flask_wtf import FlaskForm
import wtforms as form
from wtforms.validators import InputRequired, Length
from wtforms.widgets import PasswordInput


class SignInForm(FlaskForm):
    user_name = form.StringField('Username', validators=[InputRequired(), Length(0, 20)])
    password = form.StringField('Password', widget=PasswordInput(hide_value=False))