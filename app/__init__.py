# -*- coding: utf-8 -*-
import logging
import logging.handlers

from flask import Flask, g, request, current_app
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy

# Flask 확장 선언
db = SQLAlchemy()
babel = Babel()


def create_app(config=None, app_name=None):
    app_name = app_name or __name__
    app = Flask(app_name)

    app.config.from_object(config)

    # Flask 확장 초기화
    db.init_app(app)
    babel.init_app(app)

    # Logging 설정
    formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    handler = logging.handlers.RotatingFileHandler(app.config['LOGGING_LOCATION'])
    handler.setLevel(app.config['LOGGING_LEVEL'])
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    # 블루프린트 모듈 등록
    from app.blueprints.main import main as main_blueprint

    app.register_blueprint(main_blueprint, url_prefix='/')

    return app


@babel.localeselector
def get_locale():
    # 로그인한 사용자는 사용자 로케일 설정을 따른다.
    user = getattr(g, 'user', None)

    if user is not None:
        return user.locale

    # 사용자 브라우저에서 가장 적합한 언어를 선택한다.
    return request.accept_languages.best_match(current_app.config['BABEL_LANGUAGES'].keys())


@babel.timezoneselector
def get_timezone():
    user = getattr(g, 'user', None)

    if user is not None:
        return user.timezone
