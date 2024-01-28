from flask_wtf import FlaskForm
import wtforms as form
from wtforms.validators import ValidationError, InputRequired, DataRequired, Length
from wtforms.widgets import PasswordInput


class LoginForm(FlaskForm):
    username = form.StringField(label='username', validators=[DataRequired(), Length(min=4, max=20)])
    password = form.PasswordField(label='Password', validators=[DataRequired(), Length(min=4, max=20)])
    submit = form.SubmitField("Log In")


class RegisterForm(FlaskForm):
    username = form.StringField(label='username', validators=[InputRequired(), Length(min=4, max=20)])
    password = form.PasswordField(label='Password', validators=[InputRequired(), Length(min=4, max=20)])
    submit = form.SubmitField("Register")