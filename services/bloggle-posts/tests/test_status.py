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
        body = json.loads(response.data.decode())
        self.assertIn('success', body)
        self.assertIn('data', body)

    def test_status_return_correct_config(self):
        """Check status method return correct current app field."""
        response = self.client.get('/status')
        body = json.loads(response.data.decode())
        data = body.get('data')
        config = data.get('config')

        self.assertIn('DEBUG', config)
        self.assertIn('TESTING', config)

        self.assertTrue(config['DEBUG'])
        self.assertTrue(config['TESTING'])


if __name__ == '__main__':
    unittest.main()
