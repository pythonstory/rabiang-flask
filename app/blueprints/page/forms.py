# -*- coding: utf-8 -*-

from flask_babel import lazy_gettext
from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(Form):
    title = StringField(lazy_gettext('Title'), validators=[DataRequired()])
    body = TextAreaField(lazy_gettext('Body'), validators=[DataRequired()])
