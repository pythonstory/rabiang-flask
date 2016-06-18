# -*- coding: utf-8 -*-
import logging
import logging.handlers

from flask import Flask, g, request, current_app, render_template
from flask_babel import Babel
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect

# Flask Extensions can be references as global variable.
db = SQLAlchemy()
babel = Babel()
csrf = CsrfProtect()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config=None, app_name=None):
    # Create Flask App instance
    app_name = app_name or __name__
    app = Flask(app_name)

    # Load App configuration
    app.config.from_object(config)

    # Initialize Flask Extensions
    db.init_app(app)
    babel.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    # Logging Setup (Rotating File)
    formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    handler = logging.handlers.RotatingFileHandler(app.config['LOGGING_LOCATION'])
    handler.setLevel(app.config['LOGGING_LEVEL'])
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    # Register blueprint modules
    from app.blueprints.main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')

    from app.blueprints.page import page as page_blueprint
    app.register_blueprint(page_blueprint, url_prefix='/page')

    from app.blueprints.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from app.blueprints.forum import forum as forum_blueprint
    app.register_blueprint(forum_blueprint, url_prefix='/forum')

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('default/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('default/500.html'), 500

    return app


@babel.localeselector
def get_locale():
    # If logged in, load user locale settings.
    user = getattr(g, 'user', None)

    if user is not None:
        return user.locale

    # Otherwise, choose the language from user browser.
    return request.accept_languages.best_match(current_app.config['BABEL_LANGUAGES'].keys())


@babel.timezoneselector
def get_timezone():
    user = getattr(g, 'user', None)

    if user is not None:
        return user.timezone
