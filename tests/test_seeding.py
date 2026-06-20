import unittest
import sqlalchemy as sa
from app import create_app, db
from app.models import User, Deck, Card
from app.seeds import seed_db, seed_language_decks_for_user
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False

class SeedingTestCase(unittest.TestCase):
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

    def test_database_seeding_when_empty(self):
        # Verify db is empty
        user_count = db.session.scalar(sa.select(sa.func.count(User.id)))
        deck_count = db.session.scalar(sa.select(sa.func.count(Deck.id)))
        card_count = db.session.scalar(sa.select(sa.func.count(Card.id)))
        self.assertEqual(user_count, 0)
        self.assertEqual(deck_count, 0)
        self.assertEqual(card_count, 0)

        # Call seed
        result = seed_db()
        self.assertTrue(result)

        # Verify default user is created
        admin = db.session.scalar(sa.select(User).where(User.username == 'admin'))
        self.assertIsNotNone(admin)
        self.assertEqual(admin.email, 'admin@example.com')
        self.assertTrue(admin.check_password('admin123'))

        # Verify all 5 languages * 15 categories = 75 decks are created for admin
        admin_decks = db.session.scalars(sa.select(Deck).where(Deck.user_id == admin.id)).all()
        self.assertEqual(len(admin_decks), 75)

        # Verify a specific deck is created
        english_numbers_deck = db.session.scalar(
            sa.select(Deck).where(Deck.user_id == admin.id, Deck.name == 'İngilizce - Sayılar')
        )
        self.assertIsNotNone(english_numbers_deck)

        # Verify 20 cards are created for that deck
        cards = db.session.scalars(sa.select(Card).where(Card.deck_id == english_numbers_deck.id)).all()
        self.assertEqual(len(cards), 20)

    def test_database_seeding_when_not_empty_backfills(self):
        # Create a user manually
        u = User(username='testuser', email='test@example.com')
        u.set_password('password')
        db.session.add(u)
        db.session.commit()

        # At this point, testuser has 0 decks
        self.assertEqual(db.session.scalar(sa.select(sa.func.count(Deck.id))), 0)

        # Call seed on non-empty database, which should trigger backfilling for testuser
        result = seed_db()
        self.assertTrue(result)

        # Total users should still be 1 (only testuser, admin is NOT created since user_exists was True)
        user_count = db.session.scalar(sa.select(sa.func.count(User.id)))
        self.assertEqual(user_count, 1)

        # But all 75 decks should be backfilled for testuser!
        testuser_decks = db.session.scalars(sa.select(Deck).where(Deck.user_id == u.id)).all()
        self.assertEqual(len(testuser_decks), 75)

        # Verify one of the backfilled decks
        spanish_colors_deck = db.session.scalar(
            sa.select(Deck).where(Deck.user_id == u.id, Deck.name == 'İspanyolca - Renkler')
        )
        self.assertIsNotNone(spanish_colors_deck)
        
        cards_count = db.session.scalar(
            sa.select(sa.func.count(Card.id)).where(Card.deck_id == spanish_colors_deck.id)
        )
        self.assertEqual(cards_count, 20)

    def test_register_automatically_seeds_deck(self):
        # Register a new user via client
        response = self.client.post('/auth/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'Password123',
            'password_confirm': 'Password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Verify user exists
        user = db.session.scalar(sa.select(User).where(User.username == 'newuser'))
        self.assertIsNotNone(user)

        # Verify they automatically got the 15 English decks (default language 'en')
        user_decks = db.session.scalars(sa.select(Deck).where(Deck.user_id == user.id)).all()
        self.assertEqual(len(user_decks), 15)

        english_animals = db.session.scalar(
            sa.select(Deck).where(Deck.user_id == user.id, Deck.name == 'İngilizce - Hayvanlar')
        )
        self.assertIsNotNone(english_animals)
        
        cards = db.session.scalars(sa.select(Card).where(Card.deck_id == english_animals.id)).all()
        self.assertEqual(len(cards), 20)

    def test_login_automatically_seeds_deck_if_missing(self):
        # Create user manually without a deck
        u = User(username='manualuser', email='manual@example.com')
        u.set_password('password123')
        db.session.add(u)
        db.session.commit()

        # Verify no decks exist yet
        self.assertEqual(db.session.scalar(sa.select(sa.func.count(Deck.id))), 0)

        # Login user via client, which should trigger the login hook to copy the current language decks (default: 'en')
        response = self.client.post('/auth/login', data={
            'username': 'manualuser',
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Verify they got the 15 English decks
        user_decks = db.session.scalars(sa.select(Deck).where(Deck.user_id == u.id)).all()
        self.assertEqual(len(user_decks), 15)

        english_verbs = db.session.scalar(
            sa.select(Deck).where(Deck.user_id == u.id, Deck.name == 'İngilizce - En Temel Fiiller')
        )
        self.assertIsNotNone(english_verbs)

if __name__ == '__main__':
    unittest.main()
