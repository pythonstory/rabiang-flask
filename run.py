# -*- coding: utf-8 -*-
import os

from app import create_app
from app.blueprints.auth import auth
from app.blueprints.forum import forum
from app.blueprints.main import main
from app.blueprints.page import page
from app.blueprints.admin import admin

BASE_DIR = os.path.dirname(__file__)

CFG_LIST = [
    'prod.cfg',  # for production server
    'dev.cfg',   # for development
    'test.cfg'   # for test server (default)
]

for cfg in CFG_LIST:
    if os.path.isfile(os.path.join(BASE_DIR, cfg)):
        config = os.path.join(BASE_DIR, cfg)
        break

blueprints = [main, page, auth, forum, admin]

app = create_app(config=config, blueprints=blueprints)

if __name__ == '__main__':
    app.run()
