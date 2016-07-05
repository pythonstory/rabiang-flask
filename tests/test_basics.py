# -*- coding: utf-8 -*-
import unittest

from app import create_app
from app.blueprints.auth import auth
from app.blueprints.forum import forum
from app.blueprints.main import main
from app.blueprints.page import page


class BasicsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        blueprints = [main, page, auth, forum]
        app = create_app(config='../test.cfg', blueprints=blueprints)
        self.app = app.test_client()
        # db.create_all()

    def tearDown(self):
        pass
        # db.session.remove()
        # db.drop_all()

    def test_app_exists(self):
        self.assertFalse(self.app is None)

    def test_home_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)


if __name__ == '__main__':
    unittest.main()
