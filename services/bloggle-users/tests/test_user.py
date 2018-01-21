import json
import unittest

from tests.base import BaseTestCase


class UserBlueprintTestCase(BaseTestCase):
    def test_index_return_ok(self):
        """Test index return ok status."""
        self.assert200(self.client.get('/users'))

    def test_create_return_ok(self):
        """Test create return ok status."""
        self.assertStatus(self.client.post('/users', data=json.dumps({
            'email': 'test@example.com',
            'password': 'test',
        }), content_type='application/json'), 201)


if __name__ == '__main__':
    unittest.main()
