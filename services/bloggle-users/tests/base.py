from flask_testing import TestCase

from app import app, db
from config import environments


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object(environments['test'])
        return app

    def setUp(self):
        db.session.begin(subtransactions=True)

    def tearDown(self):
        db.session.rollback()
        db.session.remove()
