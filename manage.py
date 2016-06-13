# -*- coding: utf-8 -*-
from flask_script import Manager

from app import create_app

# create_app function is passed  as a callback.
manager = Manager(create_app)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.add_option('-c', '--config', dest='config', required=False, default='config')
    manager.run()
