import logging
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/app.db' % BASE_DIR
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

BABEL_LANGUAGES = {'en': 'English', 'ko': 'Korean'}
BABEL_DEFAULT_LOCALE = 'en'
BABEL_DEFAULT_TIMEZONE = 'UTC'

LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOGGING_LOCATION = 'app.log'
LOGGING_LEVEL = logging.DEBUG
