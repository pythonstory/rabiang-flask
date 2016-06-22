# -*- coding: utf-8 -*-
from flask_babel import lazy_gettext
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp

from app.utils.validators import Unique
from .models import User


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
                User,
                User.email,
                message=lazy_gettext('There is already an account '
                                     'with that email.')
            )
        ]
    )
    password = PasswordField(
        lazy_gettext('Password'),
        validators=[
            DataRequired(),
            Regexp(
                '((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{6,20})', 0,
                lazy_gettext('Weak Password')
            )
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
            Regexp('^[A-Za-z][A-Za-z0-9]*$', 0,
                   lazy_gettext('Username must have only letters or numbers')),
            Unique(
                User,
                User.username,
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
        validators=[DataRequired()])

    password = PasswordField(
        lazy_gettext('New Password'),
        validators=[
            DataRequired(),
            Regexp(
                '((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{6,20})', 0,
                lazy_gettext('Weak Password'))
        ]
    )

    password_repeat = PasswordField(
        lazy_gettext('Password Confirm'),
        validators=[
            DataRequired(),
            EqualTo('password', message=lazy_gettext('Password must match'))
        ]
    )
