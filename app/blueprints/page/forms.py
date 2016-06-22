# -*- coding: utf-8 -*-
from flask_babel import lazy_gettext
from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

from app.utils.validators import Unique
from .models import Post


class PostForm(Form):
    title = StringField(
        lazy_gettext('Title'),
        validators=[DataRequired()]
    )

    slug = StringField(
        lazy_gettext('Slug'),
        validators=[
            DataRequired(),
            Unique(Post, Post.slug, lazy_gettext('Duplicate slug'))
        ]
    )

    body = TextAreaField(
        lazy_gettext('Body'),
        validators=[DataRequired()]
    )


class CommentForm(Form):
    body = TextAreaField(
        '',
        validators=[DataRequired()]
    )
