import re
from flask import g
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, ValidationError, TextAreaField
from wtforms.validators import InputRequired, Length, EqualTo, Email
from werkzeug.security import check_password_hash
from sqlalchemy import select


class PostUpdateRecommendationForm(FlaskForm):
    title = StringField(label='Title*:', validators=[InputRequired(),
                                                     Length(min=3, max=255)])
    short_description = TextAreaField(label='Short Description*:',
                                      validators=[InputRequired(),
                                                  Length(min=5)])
    opinion = TextAreaField(label='Opinion*:', validators=[InputRequired(),
                                                           Length(min=5)])
    fiction_type = StringField(label='Type of fiction*:',
                               validators=[InputRequired(),
                                           Length(min=3, max=255)])
    tags = StringField(label='Tags:')
