# -*- coding: utf-8 -*-
from flask_babel import lazy_gettext
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp

from app.blueprints.auth.models import User
from app.utils.validators import Unique

"""
    (               # Start of group
    (?=.*\d)		# must contain one digit from 0-9
    (?=.*[a-z])		# must contain one lowercase characters
    (?=.*[A-Z])		# must contain one uppercase characters
    (?=.*\W)        # must contain one special symbols
    .               # match anything with previous condition checking
    {6,20}          # length at least 6 characters and maximum of 20
    )
"""
REGEX_STRONG_PASSWORD = '((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{6,20})'

REGEX_ALPHANUMERIC = '^[A-Za-z][A-Za-z0-9]*$'


class LoginForm(Form):
    email = StringField(
        lazy_gettext('Email'),
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        lazy_gettext('Password'),
        validators=[DataRequired()]
    )
    remember_me = BooleanField(
        lazy_gettext('Keep me logged in'),
        default=False)
    submit = SubmitField(
        lazy_gettext('Login')
    )


class RegisterForm(Form):
    email = StringField(
        lazy_gettext('Email'),
        validators=[
            DataRequired(),
            Email(),
            Unique(
                User, User.email,
                message=lazy_gettext('There is already an account '
                                     'with that email.')
            )
        ]
    )
    password = PasswordField(
        lazy_gettext('Password'),
        validators=[
            DataRequired(),
            Regexp(REGEX_STRONG_PASSWORD, 0, lazy_gettext('Weak Password'))
        ]
    )
    password_repeat = PasswordField(
        lazy_gettext('Password Confirm'),
        validators=[
            DataRequired(),
            EqualTo('password', message=lazy_gettext('Password must match'))
        ]
    )
    username = StringField(
        lazy_gettext('Username'),
        validators=[
            DataRequired(),
            Length(4, 64),
            Regexp(REGEX_ALPHANUMERIC, 0,
                   lazy_gettext('Username must have only letters or numbers')),
            Unique(
                User, User.username,
                message=lazy_gettext('There is already an account '
                                     'with that username.')
            )
        ]
    )


class UnregisterForm(Form):
    submit = SubmitField(lazy_gettext('Unregister'))


class ChangePasswordForm(Form):
    old_password = PasswordField(
        lazy_gettext('Old Password'),
        validators=[DataRequired()]
    )
    password = PasswordField(
        lazy_gettext('New Password'),
        validators=[
            DataRequired(),
            Regexp(REGEX_STRONG_PASSWORD, 0, lazy_gettext('Weak Password'))
        ]
    )
    password_repeat = PasswordField(
        lazy_gettext('Password Confirm'),
        validators=[
            DataRequired(),
            EqualTo('password', message=lazy_gettext('Password must match'))
        ]
    )
