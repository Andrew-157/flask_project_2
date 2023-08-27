import re
from flask import g
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, ValidationError
from wtforms.validators import InputRequired, Length, EqualTo, Email
from werkzeug.security import check_password_hash
from sqlalchemy import select


class PostRecommendationForm(FlaskForm):
    title = StringField(label='Title*:', validators=[InputRequired(),
                                                     Length(min=5, max=255)])
    short_description = StringField(label='Short Description*:',
                                    validators=[InputRequired(),
                                                Length(min=5)])
    opinion = StringField(label='Opinion*:', validators=[InputRequired(),
                                                         Length(min=5)])
    fiction_type = StringField(label='Type of fiction*:',
                               validators=[InputRequired(),
                                           Length(min=5, max=255)])
