import unittest
import sqlalchemy as sa
from app import create_app, db
from app.models import User, Deck, Card
from app.seeds import seed_db
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

        # Check example card
        apple_card = db.session.scalar(sa.select(Card).where(Card.word == 'Apple'))
        self.assertIsNotNone(apple_card)
        self.assertEqual(apple_card.meaning, 'Elma')
        self.assertEqual(apple_card.example_sentence, 'I eat a red apple every morning.')

    def test_database_seeding_when_not_empty(self):
        # Create a user manually
        u = User(username='testuser', email='test@example.com')
        u.set_password('password')
        db.session.add(u)
        db.session.commit()

        # Seed again
        result = seed_db()
        # Should not seed since database is not empty
        self.assertFalse(result or result is None)

        # Total users should still be 1 (only testuser, not admin)
        user_count = db.session.scalar(sa.select(sa.func.count(User.id)))
        self.assertEqual(user_count, 1)

        # Decks should be empty
        deck_count = db.session.scalar(sa.select(sa.func.count(Deck.id)))
        self.assertEqual(deck_count, 0)

if __name__ == '__main__':
    unittest.main()
