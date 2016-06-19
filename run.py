# -*- coding: utf-8 -*-
import os

from app import create_app
from app.blueprints.auth import auth
from app.blueprints.forum import forum
from app.blueprints.main import main
from app.blueprints.page import page

config = os.path.join(os.path.dirname(__file__), (os.getenv('FLASK_CONFIG') or 'test.cfg'))
blueprints = [main, page, auth, forum]

app = create_app(config=config, blueprints=blueprints)

if __name__ == '__main__':
    app.run()
