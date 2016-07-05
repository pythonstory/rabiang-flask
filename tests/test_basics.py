# -*- coding: utf-8 -*-
import unittest

from app import create_app
from app.blueprints.auth import auth
from app.blueprints.forum import forum
from app.blueprints.main import main
from app.blueprints.page import page
from app.extensions import db


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        blueprints = [main, page, auth, forum]
        app = create_app(config='../test.cfg', blueprints=blueprints)
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_app_exists(self):
        self.assertFalse(self.app is None)


if __name__ == '__main__':
    unittest.main()
