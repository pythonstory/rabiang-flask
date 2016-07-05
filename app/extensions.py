# -*- coding: utf-8 -*-
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
