# -*- coding: utf-8 -*-
from flask import request, g, current_app
from flask_babel import Babel
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CsrfProtect

"""
Flask Extensions variables are globally referenced.
"""
db = SQLAlchemy()
babel = Babel()
csrf = CsrfProtect()
login_manager = LoginManager()


# localeselector and timezoneselector decorated functions are not defined
# in the function configure_extensions of app.py module
# because it causes error when running unittest.
@babel.localeselector
def get_locale():
    # If logged in, load user locale settings.
    user = getattr(g, 'user', None)

    if user is not None:
        return user.locale

    # Otherwise, choose the language from user browser.
    return request.accept_languages.best_match(
        current_app.config['BABEL_LANGUAGES'].keys())


@babel.timezoneselector
def get_timezone():
    user = getattr(g, 'user', None)

    if user is not None:
        return user.timezone
