import unittest
from unittest.mock import patch, MagicMock
from app import create_app, db
from config import Config
from app.models import User


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False


class InlineTranslateTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # Create user
        self.user = User(username='user1', email='user1@example.com')
        self.user.set_password('password')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_translate_requires_login(self):
        response = self.client.post('/main/inline-translate', json={'text': 'Hello'})
        self.assertEqual(response.status_code, 302)

    def test_translate_empty_text(self):
        with self.client:
            self.client.post('/auth/login', data={'username': 'user1', 'password': 'password'})
            
            response = self.client.post('/main/inline-translate', json={'text': '  '})
            self.assertEqual(response.status_code, 400)
            self.assertIn('success', response.json)
            self.assertFalse(response.json['success'])

            response2 = self.client.post('/main/inline-translate', json={})
            self.assertEqual(response2.status_code, 400)

    @patch('urllib.request.urlopen')
    def test_translate_success(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"responseData": {"translatedText": "Merhaba Dunya", "match": 1}, "responseStatus": 200}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        with self.client:
            self.client.post('/auth/login', data={'username': 'user1', 'password': 'password'})
            
            response = self.client.post('/main/inline-translate', json={'text': 'Hello World'})
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.json['success'])
            self.assertEqual(response.json['translated_text'], 'Merhaba Dunya')

    @patch('urllib.request.urlopen')
    def test_translate_api_failure(self, mock_urlopen):
        # mock all urlopen calls to fail
        mock_urlopen.side_effect = Exception("Network error")

        with self.client:
            self.client.post('/auth/login', data={'username': 'user1', 'password': 'password'})
            
            response = self.client.post('/main/inline-translate', json={'text': 'Hello World'})
            self.assertEqual(response.status_code, 500)
            self.assertFalse(response.json['success'])
            self.assertIn('message', response.json)


if __name__ == '__main__':
    unittest.main()
