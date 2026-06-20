import unittest
from app import create_app, db
from config import Config
from flask import session

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False

class LanguageTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_default_language_in_session(self):
        # By default, accessing index page should initialize or work with default language 'en'
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        # Verify default language injection variables are present in context/rendered page
        # The navbar should show the default language flag (🇺🇸) and name (İngilizce)
        self.assertIn(b'\xf0\x9f\x87\xba\xf0\x9f\x87\xb8', response.data) # 🇺🇸
        self.assertIn('İngilizce'.encode('utf-8'), response.data)

    def test_set_valid_language(self):
        with self.client:
            # Set language to German (de)
            response = self.client.get('/set_language/de')
            # Should redirect (either to referrer or main index since referrer is empty)
            self.assertEqual(response.status_code, 302)
            
            # Check session variable
            self.assertEqual(session.get('learning_language'), 'de')

            # Access index and check if German language is selected
            response2 = self.client.get('/')
            self.assertIn(b'\xf0\x9f\x87\xa9\xf0\x9f\x87\xaa', response2.data) # 🇩🇪
            self.assertIn('Almanca'.encode('utf-8'), response2.data)

    def test_set_invalid_language(self):
        with self.client:
            # Try to set an invalid language
            response = self.client.get('/set_language/xyz')
            self.assertEqual(response.status_code, 302)
            
            # session['learning_language'] should not be set to xyz
            self.assertNotEqual(session.get('learning_language'), 'xyz')
            
            # Access index, should fall back to English
            response2 = self.client.get('/')
            self.assertIn('İngilizce'.encode('utf-8'), response2.data)

    def test_idioms_route_requires_login(self):
        # Accessing /idioms without login should redirect to login page
        response = self.client.get('/idioms')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/auth/login', response.headers['Location'])

    def test_idioms_route_logged_in(self):
        from app.models import User
        # Register and log in a user
        u = User(username='testuser', email='test@example.com')
        u.set_password('password')
        db.session.add(u)
        db.session.commit()
        
        # Log in the user
        self.client.post('/auth/login', data={'username': 'testuser', 'password': 'password'})
        
        # Access /idioms
        response = self.client.get('/idioms')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Popüler Kalıplar'.encode('utf-8'), response.data)
        
        # Check if the idioms are listed
        self.assertIn(b'Break a leg', response.data)
        self.assertIn('Şansın bol olsun'.encode('utf-8'), response.data)

if __name__ == '__main__':
    unittest.main()
