import unittest
from app import create_app, db
from config import Config
from app.models import User, Deck, Card

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False

class SearchTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # Create two users
        self.user1 = User(username='user1', email='user1@example.com')
        self.user1.set_password('password')
        self.user2 = User(username='user2', email='user2@example.com')
        self.user2.set_password('password')
        db.session.add_all([self.user1, self.user2])
        db.session.commit()

        # Create a deck and card for user 1
        self.deck1 = Deck(name='English - Numbers', user=self.user1)
        db.session.add(self.deck1)
        db.session.flush()

        self.card1 = Card(
            word='UniqueWordOne',
            meaning='Benzersiz Bir',
            example_sentence='This is unique word one.',
            deck=self.deck1
        )
        self.card2 = Card(
            word='UniqueWordTwo',
            meaning='Benzersiz İki',
            example_sentence='This is unique word two.',
            deck=self.deck1
        )
        db.session.add_all([self.card1, self.card2])

        # Create a deck and card for user 2
        self.deck2 = Deck(name='English - Animals', user=self.user2)
        db.session.add(self.deck2)
        db.session.flush()

        self.card_user2 = Card(
            word='UniqueWordThree',
            meaning='Benzersiz Üç',
            example_sentence='This is unique word three.',
            deck=self.deck2
        )
        db.session.add(self.card_user2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_search_requires_login(self):
        # Accessing search route unauthenticated should redirect to login page (or return 302/401)
        response = self.client.get('/search?q=UniqueWordOne')
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.headers.get('Location', '').lower())

    def test_search_empty_or_short_query(self):
        with self.client:
            # Login as user 1
            self.client.post('/auth/login', data={'username': 'user1', 'password': 'password'})
            
            # Test empty query
            response = self.client.get('/search?q=')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, [])

            # Test short query (1 character)
            response = self.client.get('/search?q=u')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, [])

    def test_search_valid_results(self):
        with self.client:
            # Login as user 1
            self.client.post('/auth/login', data={'username': 'user1', 'password': 'password'})

            # Search case-insensitive 'uniquewordone'
            response = self.client.get('/search?q=uNiQuEwOrDoNe')
            self.assertEqual(response.status_code, 200)
            results = response.json
            self.assertEqual(len(results), 1)
            
            # Verify fields
            card_json = results[0]
            self.assertEqual(card_json['word'], 'UniqueWordOne')
            self.assertEqual(card_json['meaning'], 'Benzersiz Bir')
            self.assertEqual(card_json['example_sentence'], 'This is unique word one.')
            self.assertEqual(card_json['example_meaning'], '')

    def test_search_scope_user_only(self):
        with self.client:
            # Login as user 1
            self.client.post('/auth/login', data={'username': 'user1', 'password': 'password'})

            # Search for 'UniqueWordThree' (which belongs to user 2)
            response = self.client.get('/search?q=uniquewordthree')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, [])

            # Logout
            self.client.get('/auth/logout')

            # Login as user 2
            self.client.post('/auth/login', data={'username': 'user2', 'password': 'password'})

            # Search for 'UniqueWordThree' (should succeed now)
            response = self.client.get('/search?q=uniquewordthree')
            self.assertEqual(response.status_code, 200)
            results = response.json
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0]['word'], 'UniqueWordThree')

            # Search for 'UniqueWordOne' (belongs to user 1, user 2 should not see it)
            response2 = self.client.get('/search?q=uniquewordone')
            self.assertEqual(response2.status_code, 200)
            self.assertEqual(response2.json, [])

if __name__ == '__main__':
    unittest.main()
