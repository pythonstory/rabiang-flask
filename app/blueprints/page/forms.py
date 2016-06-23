# -*- coding: utf-8 -*-
from flask_babel import lazy_gettext
from flask_wtf import Form
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired

from app.utils.validators import Unique
from .models import Post


class PostForm(Form):
    title = StringField(
        lazy_gettext('Post Title'),
        validators=[DataRequired()]
    )
    slug = StringField(
        lazy_gettext('Post Slug'),
        validators=[
            DataRequired(),
            Unique(Post, Post.slug, lazy_gettext('Duplicate slug'))
        ]
    )
    body = TextAreaField(
        lazy_gettext('Post Body'),
        validators=[DataRequired()]
    )
    status = SelectField(
        lazy_gettext('Post Status'),
        choices=(
            (Post.STATUS_DRAFT, lazy_gettext('Draft')),
            (Post.STATUS_PUBLIC, lazy_gettext('Public')),
            (Post.STATUS_PRIVATE, lazy_gettext('Private'))),
        coerce=int)


class CommentForm(Form):
    body = TextAreaField(
        '',
        validators=[DataRequired()]
    )
