import unittest
from app import create_app, db
from app.models import User, Deck, Card
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False

class StudyTestCase(unittest.TestCase):
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

    def test_study_route_requires_login(self):
        # Accessing study route unauthenticated should redirect to login page
        response = self.client.get('/deck/1/study')
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.headers.get('Location', '').lower())

    def test_study_empty_deck_redirects(self):
        # Create a test user
        u = User(username='test', email='test@example.com')
        u.set_password('password')
        db.session.add(u)
        db.session.commit()

        # Login
        with self.client:
            self.client.post('/auth/login', data={'username': 'test', 'password': 'password'})
            
            # Create a deck
            d = Deck(name='Test Deck', user=u)
            db.session.add(d)
            db.session.commit()

            # Empty deck study should redirect back to deck details
            response = self.client.get(f'/deck/{d.id}/study')
            self.assertEqual(response.status_code, 302)
            self.assertIn(f'/deck/{d.id}', response.headers.get('Location', ''))

    def test_study_valid_deck_with_cards(self):
        # Create user, login, deck, cards, and check successful study load
        u = User(username='test', email='test@example.com')
        u.set_password('password')
        db.session.add(u)
        db.session.commit()

        with self.client:
            self.client.post('/auth/login', data={'username': 'test', 'password': 'password'})
            
            d = Deck(name='Test Deck', user=u)
            db.session.add(d)
            db.session.commit()

            c1 = Card(word='Apple', meaning='Elma', example_sentence='I eat an apple.', deck=d)
            c2 = Card(word='Book', meaning='Kitap', example_sentence='Read a book.', deck=d)
            db.session.add_all([c1, c2])
            db.session.commit()

            response = self.client.get(f'/deck/{d.id}/study')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Apple', response.data)
            self.assertIn(b'Book', response.data)

    def test_game_route_requires_login(self):
        # Accessing game route unauthenticated should redirect to login page
        response = self.client.get('/deck/1/game')
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.headers.get('Location', '').lower())

    def test_game_empty_deck_redirects(self):
        # Create a test user
        u = User(username='test_game', email='test_game@example.com')
        u.set_password('password')
        db.session.add(u)
        db.session.commit()

        # Login
        with self.client:
            self.client.post('/auth/login', data={'username': 'test_game', 'password': 'password'})
            
            # Create a deck
            d = Deck(name='Test Deck Game', user=u)
            db.session.add(d)
            db.session.commit()

            # Empty deck game should redirect back to deck details
            response = self.client.get(f'/deck/{d.id}/game')
            self.assertEqual(response.status_code, 302)
            self.assertIn(f'/deck/{d.id}', response.headers.get('Location', ''))

    def test_game_valid_deck_with_cards(self):
        # Create user, login, deck, cards, and check successful game load
        u = User(username='test_game_valid', email='test_game_valid@example.com')
        u.set_password('password')
        db.session.add(u)
        db.session.commit()

        with self.client:
            self.client.post('/auth/login', data={'username': 'test_game_valid', 'password': 'password'})
            
            d = Deck(name='Test Deck Game Valid', user=u)
            db.session.add(d)
            db.session.commit()

            c1 = Card(word='Apple', meaning='Elma', example_sentence='I eat an apple.', deck=d)
            c2 = Card(word='Book', meaning='Kitap', example_sentence='Read a book.', deck=d)
            db.session.add_all([c1, c2])
            db.session.commit()

            response = self.client.get(f'/deck/{d.id}/game')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Apple', response.data)
            self.assertIn(b'Book', response.data)

if __name__ == '__main__':
    unittest.main()
