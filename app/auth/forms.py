from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, ValidationError
from wtforms.validators import InputRequired, Length, EqualTo
from sqlalchemy import select

from .. import db
from ..models import User
from .crud import get_user_with_username, get_user_with_email


class RegisterForm(FlaskForm):
    username = StringField(label='Username*:', validators=[InputRequired(),
                                                         Length(min=5, max=255)])
    email = EmailField(label='Email*:', validators=[InputRequired(),
                                                  Length(max=255)])
    password1 = PasswordField(label='Password*:', validators=[InputRequired(),
                                                            Length(min=8, max=255)])
    password2 = PasswordField(label='Password confirmation*:', validators=[InputRequired(),
                                                                         Length(min=8, max=255),
                                                                           EqualTo('password1', message='Passwords did not match')])

    def validate_username(self, field):
        user_with_username = get_user_with_username(username=field.data)
        if user_with_username:
            raise ValidationError(message='A user with this username already exists.')
        allowed_symbols = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ@.+-_"
        for symbol in field.data:
            if symbol not in allowed_symbols:
                raise ValidationError(
                    message='Username is not valid.Letters, digits and @/./+/-/_ only.')
        
    def validate_email(self, field):
        user_with_email = get_user_with_email(email=field.data)
        if user_with_email:
            raise ValidationError(message='A user with this email already exists.')
