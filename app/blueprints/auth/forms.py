# -*- coding: utf-8 -*-

from flask_babel import lazy_gettext
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField


class LoginForm(Form):
    email = StringField(lazy_gettext('Email'))
    password = PasswordField(lazy_gettext('Password'))
    remember_me = BooleanField(lazy_gettext('Keep me logged in'))
    submit = SubmitField(lazy_gettext('Login'))


class RegisterForm(Form):
    email = StringField(lazy_gettext('Email'))
    password = PasswordField(lazy_gettext('Password'))
    password_repeat = PasswordField(lazy_gettext('Password'))
    username = StringField(lazy_gettext('Username'))
