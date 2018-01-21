import os
import unittest

from flask_migrate import Migrate

from common import create_app, db

app = create_app(os.getenv('APP_ENV'))
migrate = Migrate(app, db)


@app.cli.command()
def test():
    """Runs the tests without code coverage."""
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1
