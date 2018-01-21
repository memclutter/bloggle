import json
import unittest

from tests.base import BaseTestCase


class StatusBlueprintTestCase(BaseTestCase):
    """Tests for status blueprint."""

    def test_status_return_ok(self):
        """Check status method return ok."""
        self.assert200(self.client.get('/status'))

    def test_status_return_correct_body(self):
        """Check status method return correct body."""
        response = self.client.get('/status')
        data = json.loads(response.data.decode())
        self.assertIn('success', data)
        self.assertIn('time', data)
        self.assertIn('current_app', data)

    def test_status_return_correct_current_app_field(self):
        """Check status method return correct current app field."""
        response = self.client.get('/status')
        data = json.loads(response.data.decode())
        current_app = data['current_app']

        self.assertIn('debug', current_app)
        self.assertIn('testing', current_app)

        self.assertTrue(current_app['debug'])
        self.assertTrue(current_app['testing'])


if __name__ == '__main__':
    unittest.main()
