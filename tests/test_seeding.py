import unittest
import sqlalchemy as sa
from app import create_app, db
from app.models import User, Deck, Card
from app.seeds import seed_db, seed_default_deck_for_user
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

        # Verify deck is created
        deck = db.session.scalar(sa.select(Deck).where(Deck.user_id == admin.id))
        self.assertIsNotNone(deck)
        self.assertEqual(deck.name, 'A1-A2 Seviyesi Yaygın Kelimeler')

        # Verify 20 cards are created
        cards = db.session.scalars(sa.select(Card).where(Card.deck_id == deck.id)).all()
        self.assertEqual(len(cards), 20)

    def test_database_seeding_when_not_empty_backfills(self):
        # Create a user manually
        u = User(username='testuser', email='test@example.com')
        u.set_password('password')
        db.session.add(u)
        db.session.commit()

        # At this point, testuser has 0 decks
        self.assertEqual(db.session.scalar(sa.select(sa.func.count(Deck.id))), 0)

        # Call seed on non-empty database, which should trigger backfilling
        result = seed_db()
        self.assertTrue(result)

        # Total users should still be 1 (only testuser, admin is NOT created since user_exists was True)
        user_count = db.session.scalar(sa.select(sa.func.count(User.id)))
        self.assertEqual(user_count, 1)

        # But the deck should be backfilled for testuser!
        deck = db.session.scalar(sa.select(Deck).where(Deck.user_id == u.id))
        self.assertIsNotNone(deck)
        self.assertEqual(deck.name, 'A1-A2 Seviyesi Yaygın Kelimeler')

        # Verify 20 cards are created for it
        cards_count = db.session.scalar(sa.select(sa.func.count(Card.id)))
        self.assertEqual(cards_count, 20)

    def test_register_automatically_seeds_deck(self):
        # Register a new user via client
        response = self.client.post('/auth/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'password_confirm': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Verify user exists
        user = db.session.scalar(sa.select(User).where(User.username == 'newuser'))
        self.assertIsNotNone(user)

        # Verify they automatically got the A1-A2 deck
        deck = db.session.scalar(sa.select(Deck).where(Deck.user_id == user.id))
        self.assertIsNotNone(deck)
        self.assertEqual(deck.name, 'A1-A2 Seviyesi Yaygın Kelimeler')
        
        cards = db.session.scalars(sa.select(Card).where(Card.deck_id == deck.id)).all()
        self.assertEqual(len(cards), 20)

    def test_login_automatically_seeds_deck_if_missing(self):
        # Create user manually without a deck
        u = User(username='manualuser', email='manual@example.com')
        u.set_password('password123')
        db.session.add(u)
        db.session.commit()

        # Verify no decks exist yet
        self.assertEqual(db.session.scalar(sa.select(sa.func.count(Deck.id))), 0)

        # Login user via client, which should trigger the login hook to copy the deck
        response = self.client.post('/auth/login', data={
            'username': 'manualuser',
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Verify deck has been copied/seeded for them
        deck = db.session.scalar(sa.select(Deck).where(Deck.user_id == u.id))
        self.assertIsNotNone(deck)
        self.assertEqual(deck.name, 'A1-A2 Seviyesi Yaygın Kelimeler')

if __name__ == '__main__':
    unittest.main()
