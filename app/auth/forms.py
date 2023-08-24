from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Length


class RegisterForm(FlaskForm):
    username = StringField(label='Username', validators=[InputRequired(),
                                                         Length(min=5, max=255)])
    email = EmailField(label='Email', validators=[InputRequired(),
                                                  Length(max=255)])
    password1 = PasswordField(label='Password', validators=[InputRequired(),
                                                            Length(min=8, max=255)])
    password2 = PasswordField(label='Password Confirmation', validators=[InputRequired(),
                                                                         Length(min=8, max=255)])
