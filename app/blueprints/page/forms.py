# -*- coding: utf-8 -*-
from flask_babel import lazy_gettext
from flask_wtf import Form, RecaptchaField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, SubmitField, \
    IntegerField
from wtforms.validators import DataRequired, Email, Optional

from app.blueprints.page.models import Post, Tag
from app.utils.validators import Unique


class TagField(StringField):
    def _value(self):
        """
        Converts the list of Tag instances into
        a comma-separated list of tag names

        Called when rendering form
        """
        if self.data:
            # Display tags as a comma-separated list.
            return ','.join([tag.name for tag in self.data])

        return ''

    def process_formdata(self, valuelist):
        """
        Accepts the comma-separated tag list
        and converts it into a list of Tag instances

        Called when creating TagField instance
        """
        if valuelist:
            self.data = self.get_tags_from_string(valuelist[0])
        else:
            self.data = []

    def get_tags_from_string(self, tag_string):
        # User input comma-separated tags
        raw_tags = tag_string.split(',')

        # Strip whitespaces from user input tags
        tag_names = [name.strip() for name in raw_tags if name.strip()]

        # Query the database and retrieve any tags we have already saved.
        existing_tags = Tag.query.filter(Tag.name.in_(tag_names))

        # Determine which tag names are new.
        new_names = set(tag_names) - set([tag.name for tag in existing_tags])

        # Create a list of unsaved Tag instances for the new tags.
        new_tags = [Tag(name=name) for name in new_names]

        # Return all the existing tags + all the new, unsaved tags.
        return list(existing_tags) + new_tags


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
            (Post.STATUS_PUBLIC, lazy_gettext('Public'))),
        coerce=int)
    tags = TagField(
        lazy_gettext('Tag'),
        description=lazy_gettext('Separate multiple tags with commas. '
                                 'All of whitespaces are ignored.')
    )
    category = SelectField(
        lazy_gettext('Category'),
        coerce=int
    )


class CommentForm(Form):
    name = StringField(
        lazy_gettext('Name'),
        validators=[DataRequired()]
    )
    email = StringField(
        lazy_gettext('Email'),
        validators=[DataRequired(), Email()]
    )
    body = TextAreaField(
        lazy_gettext('Comment'),
        validators=[DataRequired()]
    )
    recaptcha = RecaptchaField()


class DeletePostForm(Form):
    submit = SubmitField(
        lazy_gettext('Delete')
    )


class CategoryForm(Form):
    name = StringField(
        lazy_gettext('Name'),
        validators=[DataRequired()]
    )
    order = IntegerField(
        lazy_gettext('Order'),
        validators=[DataRequired()]
    )
    parent = SelectField(
        lazy_gettext('Parent Category'),
        validators=[Optional()],
        coerce=int
    )


class DeleteCategoryForm(Form):
    submit = SubmitField(
        lazy_gettext('Delete')
    )


class PhotoForm(Form):
    photo = FileField(
        'Your photo',
        validators=[
            FileRequired(),
            FileAllowed(['jpg', 'jpe', 'jpeg', 'png', 'gif', 'svg', 'bmp'],
                        'Images only!')]
    )
