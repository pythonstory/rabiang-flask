# -*- coding: utf-8 -*-
from flask_babel import lazy_gettext
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email

from .models import User


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

    def validate(self):
        rv = Form.validate(self)

        if not rv:
            return False

        user = User.query.filter_by(email=self.email.data).first()

        if user is not None:
            self.email.errors.append(lazy_gettext('Email already exists.'))
            return False

        user = User.query.filter_by(username=self.username.data).first()

        if user is not None:
            self.username.errors.append(lazy_gettext('Username already exists.'))
            return False

        return True