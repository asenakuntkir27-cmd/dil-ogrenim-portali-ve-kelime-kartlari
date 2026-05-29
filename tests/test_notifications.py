import unittest
from app import create_app, db
from config import Config
from app.models import User

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False

class NotificationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # Create user
        self.user = User(username='sena', email='sena@example.com', daily_target=10)
        self.user.set_password('password')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_status_requires_login(self):
        response = self.client.get('/api/user-status')
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.headers.get('Location', '').lower())

    def test_user_status_authenticated(self):
        with self.client:
            # Login
            self.client.post('/auth/login', data={'username': 'sena', 'password': 'password'})

            response = self.client.get('/api/user-status')
            self.assertEqual(response.status_code, 200)
            data = response.json
            self.assertEqual(data['username'], 'sena')
            self.assertEqual(data['daily_target'], 10)
            self.assertEqual(data['today_count'], 0)
            self.assertEqual(data['remaining'], 10)
            self.assertEqual(data['current_streak'], 1)

            # Record some activity to verify changes in today_count and remaining
            self.user.record_activity(3)
            db.session.commit()

            response = self.client.get('/api/user-status')
            self.assertEqual(response.status_code, 200)
            data = response.json
            self.assertEqual(data['today_count'], 3)
            self.assertEqual(data['remaining'], 7)

if __name__ == '__main__':
    unittest.main()
