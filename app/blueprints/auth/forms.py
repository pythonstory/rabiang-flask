# -*- coding: utf-8 -*-
from flask_babel import lazy_gettext
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email

from app.utils.validators import Unique, StrongPassword
from .models import User


class LoginForm(Form):
    email = StringField(lazy_gettext('Email'),
                        validators=[DataRequired(), Email()])
    password = PasswordField(lazy_gettext('Password'),
                             validators=[DataRequired()])
    remember_me = BooleanField(lazy_gettext('Keep me logged in'), default=False)
    submit = SubmitField(lazy_gettext('Login'))


class RegisterForm(Form):
    email = StringField(lazy_gettext('Email'),
                        validators=[DataRequired(), Email(),
                                    Unique(User, User.email,
                                           message=lazy_gettext('There is already an account with that email.'))])
    password = PasswordField(lazy_gettext('Password'),
                             validators=[DataRequired(), StrongPassword(message=lazy_gettext('Weak Password'))])
    password_repeat = PasswordField(lazy_gettext('Password'),
                                    validators=[DataRequired()])
    username = StringField(lazy_gettext('Username'),
                           validators=[DataRequired(),
                                       Unique(User, User.username,
                                              message=lazy_gettext('There is already an account with that username.'))])
