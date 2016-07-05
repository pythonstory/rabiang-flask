# -*- coding: utf-8 -*-
from flask import request, g, current_app
from flask_babel import Babel
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CsrfProtect

"""
Flask Extensions can be references as global variable.
"""
db = SQLAlchemy()
babel = Babel()
csrf = CsrfProtect()
login_manager = LoginManager()


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
