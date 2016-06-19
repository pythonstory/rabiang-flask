# -*- coding: utf-8 -*-
from flask_babel import lazy_gettext
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email


class LoginForm(Form):
    email = StringField(lazy_gettext('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(lazy_gettext('Password'), validators=[DataRequired()])
    remember_me = BooleanField(lazy_gettext('Keep me logged in'), default=False)
    submit = SubmitField(lazy_gettext('Login'))


class RegisterForm(Form):
    email = StringField(lazy_gettext('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(lazy_gettext('Password'), validators=[DataRequired()])
    password_repeat = PasswordField(lazy_gettext('Password'), validators=[DataRequired()])
    username = StringField(lazy_gettext('Username'), validators=[DataRequired()])
