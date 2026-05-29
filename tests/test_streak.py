import unittest
from datetime import date, timedelta
from app import create_app, db
from config import Config
from app.models import User, Deck, Card

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False

class StreakTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # Create test user
        self.user = User(username='streak_player', email='sp@example.com')
        self.user.set_password('pass')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_streak_defaults(self):
        self.assertEqual(self.user.current_streak, 0)
        self.assertIsNone(self.user.last_activity_date)
        self.assertEqual(self.user.daily_target, 10)
        self.assertEqual(self.user.daily_progress, 0)
        self.assertEqual(self.user.streak, 0)
        self.assertEqual(self.user.get_daily_progress(), 0)

    def test_record_activity_first_time(self):
        self.user.record_activity(3)
        db.session.commit()

        self.assertEqual(self.user.current_streak, 1)
        self.assertEqual(self.user.last_activity_date, date.today())
        self.assertEqual(self.user.daily_progress, 3)
        self.assertEqual(self.user.streak, 1)
        self.assertEqual(self.user.get_daily_progress(), 3)

    def test_record_activity_same_day(self):
        self.user.record_activity(3)
        self.user.record_activity(4)
        db.session.commit()

        self.assertEqual(self.user.current_streak, 1)
        self.assertEqual(self.user.last_activity_date, date.today())
        self.assertEqual(self.user.daily_progress, 7)
        self.assertEqual(self.user.streak, 1)
        self.assertEqual(self.user.get_daily_progress(), 7)

    def test_record_activity_next_day(self):
        # Set last activity to yesterday
        self.user.last_activity_date = date.today() - timedelta(days=1)
        self.user.current_streak = 1
        self.user.daily_progress = 10
        db.session.commit()

        # Today's first activity
        self.user.record_activity(5)
        db.session.commit()

        self.assertEqual(self.user.current_streak, 2)
        self.assertEqual(self.user.last_activity_date, date.today())
        self.assertEqual(self.user.daily_progress, 5) # reset and set to new points
        self.assertEqual(self.user.streak, 2)
        self.assertEqual(self.user.get_daily_progress(), 5)

    def test_record_activity_broken_streak(self):
        # Set last activity to 2 days ago
        self.user.last_activity_date = date.today() - timedelta(days=2)
        self.user.current_streak = 5
        self.user.daily_progress = 10
        db.session.commit()

        # Today's first activity
        self.user.record_activity(4)
        db.session.commit()

        self.assertEqual(self.user.current_streak, 1) # reset to 1
        self.assertEqual(self.user.last_activity_date, date.today())
        self.assertEqual(self.user.daily_progress, 4)
        self.assertEqual(self.user.streak, 1)
        self.assertEqual(self.user.get_daily_progress(), 4)

    def test_streak_property_returns_zero_on_inactive(self):
        self.user.current_streak = 5
        self.user.last_activity_date = date.today() - timedelta(days=2)
        db.session.commit()

        # User is inactive for 2 days, so streak property should evaluate to 0
        self.assertEqual(self.user.streak, 0)
        self.assertEqual(self.user.get_daily_progress(), 0)

    def test_dashboard_login_activity_update(self):
        with self.client:
            self.client.post('/auth/login', data={'username': 'streak_player', 'password': 'pass'})
            
            # Fetch user from db to verify activity is updated
            user_db = db.session.get(User, self.user.id)
            self.assertEqual(user_db.last_activity_date, date.today())
            self.assertEqual(user_db.current_streak, 1)
            self.assertEqual(user_db.daily_progress, 0) # login adds 0 points

    def test_api_study_complete_requires_login(self):
        response = self.client.post('/api/v1/study/complete', json={'cards_count': 5})
        self.assertEqual(response.status_code, 302)

    def test_api_study_complete_adds_points(self):
        with self.client:
            self.client.post('/auth/login', data={'username': 'streak_player', 'password': 'pass'})
            
            response = self.client.post('/api/v1/study/complete', json={'cards_count': 7})
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.json['success'])

            user_db = db.session.get(User, self.user.id)
            self.assertEqual(user_db.get_daily_progress(), 7)

if __name__ == '__main__':
    unittest.main()
