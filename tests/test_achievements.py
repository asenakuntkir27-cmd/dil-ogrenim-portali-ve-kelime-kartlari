import unittest
from datetime import date
import sqlalchemy as sa
from app import create_app, db
from app.models import User, Deck, Score
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False

class AchievementsTestCase(unittest.TestCase):
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

    def test_achievements_first_spark(self):
        # Create user with streak < 3, and last activity date is today so login won't reset it
        u = User(username='user1', email='user1@example.com', current_streak=2, last_activity_date=date.today())
        u.set_password('password123')
        db.session.add(u)
        db.session.commit()

        with self.client:
            self.client.post('/auth/login', data={'username': 'user1', 'password': 'password123'})
            
            # Access profile page - badge_first_spark should be False
            response = self.client.get('/profile')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Kilitli (Streak: 2/3)', response.data)

        # Update user streak to 3
        with self.app.app_context():
            u_db = db.session.get(User, u.id)
            u_db.current_streak = 3
            db.session.commit()

        with self.client:
            # Re-access profile page - badge_first_spark should be True
            response = self.client.get('/profile')
            self.assertEqual(response.status_code, 200)
            self.assertNotIn(b'Kilitli (Streak: 3/3)', response.data)
            self.assertIn(b'Kazan\xc4\xb1ld\xc4\xb1', response.data) # "Kazanıldı" in UTF-8

    def test_achievements_word_pro(self):
        # Create user with no high scores
        u = User(username='user2', email='user2@example.com')
        u.set_password('password123')
        db.session.add(u)
        db.session.commit()

        with self.client:
            self.client.post('/auth/login', data={'username': 'user2', 'password': 'password123'})
            
            # Access profile page - badge_word_pro should be False
            response = self.client.get('/profile')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Kilitli (Hedef: 100+ Puan)', response.data)

        # Add a score < 100
        score1 = Score(user_id=u.id, game_name="Kelime Eşleştirme", score=50)
        db.session.add(score1)
        db.session.commit()

        with self.client:
            # Access profile page - badge_word_pro should still be False
            response = self.client.get('/profile')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Kilitli (Hedef: 100+ Puan)', response.data)

        # Add a score >= 100
        score2 = Score(user_id=u.id, game_name="Kelime Tetrisi", score=105)
        db.session.add(score2)
        db.session.commit()

        with self.client:
            # Access profile page - badge_word_pro should be True
            response = self.client.get('/profile')
            self.assertEqual(response.status_code, 200)
            self.assertNotIn(b'Kilitli (Hedef: 100+ Puan)', response.data)

    def test_achievements_deck_collector(self):
        # Create user
        u = User(username='user3', email='user3@example.com')
        u.set_password('password123')
        db.session.add(u)
        db.session.commit()

        with self.client:
            self.client.post('/auth/login', data={'username': 'user3', 'password': 'password123'})
            
            # Delete auto-seeded decks from the login trigger to get a clean state
            with self.app.app_context():
                db.session.execute(sa.delete(Deck).where(Deck.user_id == u.id))
                db.session.commit()

            # Now add exactly 4 manual decks
            with self.app.app_context():
                for i in range(4):
                    d = Deck(name=f"Deste {i}", user_id=u.id)
                    db.session.add(d)
                db.session.commit()
            
            # Access profile page - badge_deck_collector should be False
            response = self.client.get('/profile')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Kilitli (Deste: 4/5)', response.data)

        # Add a 5th deck
        with self.app.app_context():
            d5 = Deck(name="Deste 5", user_id=u.id)
            db.session.add(d5)
            db.session.commit()

        with self.client:
            # Access profile page - badge_deck_collector should be True
            response = self.client.get('/profile')
            self.assertEqual(response.status_code, 200)
            self.assertNotIn(b'Kilitli (Deste: 5/5)', response.data)
