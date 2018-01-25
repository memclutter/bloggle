import unittest

from flask import json

from blueprints.user import User
from common import db
from tests.base import BaseTestCase


class UserIndexTestCase(BaseTestCase):
    def test_index_return_ok(self):
        """Test index return ok status."""
        self.assert200(self.client.get('/users'))

    def test_index_filter_by_email_return_ok(self):
        """Test index filter by email return ok"""
        db.session.add(User(email='john@example.com', password='test'))
        db.session.add(User(email='garry@example.com', password='test'))
        db.session.add(User(email='amanda@example.com', password='test'))
        db.session.commit()

        response = self.client.get('/users?email=john@example.com')
        data = json.loads(response.data)['data']

        self.assert200(response)
        self.assertIn('items', data)
        self.assertEqual(len(data['items']), 1)
        self.assertEqual(data['items'][0]['email'], 'john@example.com')

    def test_index_filter_by_first_name_return_ok(self):
        """Test index filter by first name return ok"""
        db.session.add(User(email='john@example.com', password='test', first_name='John'))
        db.session.add(User(email='garry@example.com', password='test', first_name='Garry'))
        db.session.add(User(email='amanda@example.com', password='test', first_name='Amanda'))
        db.session.commit()

        response = self.client.get('/users?first_name=garry')
        data = json.loads(response.data)['data']

        self.assert200(response)
        self.assertIn('items', data)
        self.assertEqual(len(data['items']), 1)
        self.assertEqual(data['items'][0]['first_name'], 'Garry')

    def test_index_filter_by_last_name_return_ok(self):
        """Test index filter by last name return ok."""
        db.session.add(User(email='john.doe@example.com', password='test', last_name='Doe'))
        db.session.add(User(email='garry.brow@example.com', password='test', last_name='Brow'))
        db.session.add(User(email='amanda.sanchez@example.com', password='test', last_name='Sanchez'))
        db.session.commit()

        response = self.client.get('/users?last_name=sanchez')
        data = json.loads(response.data)['data']

        self.assert200(response)
        self.assertIn('items', data)
        self.assertEqual(len(data['items']), 1)
        self.assertEqual(data['items'][0]['last_name'], 'Sanchez')

    def test_index_search_by_email_return_ok(self):
        """Test index search by email return ok."""
        db.session.add(User(email='john.doe@example.com', password='test', first_name='John', last_name='Doe'))
        db.session.add(User(email='garry.brow@example.com', password='test', first_name='Garry', last_name='Brow'))
        db.session.add(User(email='amanda.sanchez@example.com', password='test', first_name='Amanda', last_name='Sanchez'))
        db.session.commit()

        response = self.client.get('/users?search=@example.com')
        data = json.loads(response.data)['data']

        self.assert200(response)
        self.assertIn('items', data)
        self.assertEqual(len(data['items']), 3)


class UserCreateTestCase(BaseTestCase):
    def test_create_return_ok(self):
        """Test create return ok status."""
        self.assertStatus(self.client.post('/users', data=json.dumps({
            'email': 'test@example.com',
            'password': 'test',
        }), content_type='application/json'), 201)

    def test_create_with_invalid_payload_return_400(self):
        """Test create method with invalid payload return 400."""
        self.assert400(self.client.post('/users'))

    def test_create_with_empty_email_return_422(self):
        """Test create with empty email return 422."""
        self.assertStatus(self.client.post('/users', data=json.dumps({
            'password': 'test',
        }), content_type='application/json'), 422)

    def test_create_with_empty_password_return_422(self):
        """Test create with empty password return 422."""
        self.assertStatus(self.client.post('/users', data=json.dumps({
            'email': 'test@example.com',
        }), content_type='application/json'), 422)

    def test_create_with_invalid_email_return_422(self):
        """Test create with invalid email return 422."""
        self.assertStatus(self.client.post('/users', data=json.dumps({
            'email': 'test',
            'password': 'test',
        }), content_type='application/json'), 422)

    def test_create_with_already_use_email_return_422(self):
        """Test create with already use email return 422."""
        db.session.add(User(email='test@example.com', password='test'))
        db.session.commit()

        self.assertStatus(self.client.post('/users', data=json.dumps({
            'email': 'test@example.com',
            'password': 'test',
        }), content_type='application/json'), 422)


if __name__ == '__main__':
    unittest.main()
