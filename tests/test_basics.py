# -*- coding: utf-8 -*-
import unittest

from app import create_app, db
from app.blueprints.auth import auth
from app.blueprints.forum import forum
from app.blueprints.main import main
from app.blueprints.page import page


class BasicsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        blueprints = [main, page, auth, forum]

        app = create_app(config='../test.cfg', blueprints=blueprints)
        cls.app = app.test_client()

        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()

    def test_app_exists(self):
        self.assertFalse(BasicsTestCase.app is None)


if __name__ == '__main__':
    unittest.main()
