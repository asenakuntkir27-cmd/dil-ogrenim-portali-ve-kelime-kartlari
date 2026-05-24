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

    def test_word_drop_route_requires_login(self):
        response = self.client.get('/deck/1/word-drop')
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.headers.get('Location', '').lower())

    def test_word_drop_empty_deck_redirects(self):
        u = User(username='test_wd_empty', email='test_wd_empty@example.com')
        u.set_password('password')
        db.session.add(u)
        db.session.commit()

        with self.client:
            self.client.post('/auth/login', data={'username': 'test_wd_empty', 'password': 'password'})
            
            d = Deck(name='Test Deck WD Empty', user=u)
            db.session.add(d)
            db.session.commit()

            response = self.client.get(f'/deck/{d.id}/word-drop')
            self.assertEqual(response.status_code, 302)
            self.assertIn(f'/deck/{d.id}', response.headers.get('Location', ''))

    def test_word_drop_valid_deck_with_cards(self):
        u = User(username='test_wd_valid', email='test_wd_valid@example.com')
        u.set_password('password')
        db.session.add(u)
        db.session.commit()

        with self.client:
            self.client.post('/auth/login', data={'username': 'test_wd_valid', 'password': 'password'})
            
            d = Deck(name='Test Deck WD Valid', user=u)
            db.session.add(d)
            db.session.commit()

            c1 = Card(word='Apple', meaning='Elma', example_sentence='I eat an apple.', deck=d)
            c2 = Card(word='Book', meaning='Kitap', example_sentence='Read a book.', deck=d)
            db.session.add_all([c1, c2])
            db.session.commit()

            response = self.client.get(f'/deck/{d.id}/word-drop')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Apple', response.data)
            self.assertIn(b'Book', response.data)

    def test_sentence_builder_route_requires_login(self):
        response = self.client.get('/deck/1/sentence-builder')
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.headers.get('Location', '').lower())

    def test_sentence_builder_empty_deck_redirects(self):
        u = User(username='test_sb_empty', email='test_sb_empty@example.com')
        u.set_password('password')
        db.session.add(u)
        db.session.commit()

        with self.client:
            self.client.post('/auth/login', data={'username': 'test_sb_empty', 'password': 'password'})
            
            d = Deck(name='Test Deck SB Empty', user=u)
            db.session.add(d)
            db.session.commit()

            # Empty deck (no example sentence cards) should redirect
            response = self.client.get(f'/deck/{d.id}/sentence-builder')
            self.assertEqual(response.status_code, 302)
            self.assertIn(f'/deck/{d.id}', response.headers.get('Location', ''))

    def test_sentence_builder_valid_deck_with_cards(self):
        u = User(username='test_sb_valid', email='test_sb_valid@example.com')
        u.set_password('password')
        db.session.add(u)
        db.session.commit()

        with self.client:
            self.client.post('/auth/login', data={'username': 'test_sb_valid', 'password': 'password'})
            
            d = Deck(name='Test Deck SB Valid', user=u)
            db.session.add(d)
            db.session.commit()

            c1 = Card(word='Apple', meaning='Elma', example_sentence='I eat an apple.', deck=d)
            c2 = Card(word='Book', meaning='Kitap', example_sentence='Read a book.', deck=d)
            db.session.add_all([c1, c2])
            db.session.commit()

            response = self.client.get(f'/deck/{d.id}/sentence-builder')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Apple', response.data)
            self.assertIn(b'Book', response.data)

    def test_memory_flip_route_requires_login(self):
        response = self.client.get('/deck/1/memory-flip')
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.headers.get('Location', '').lower())

    def test_memory_flip_empty_deck_redirects(self):
        u = User(username='test_mf_empty', email='test_mf_empty@example.com')
        u.set_password('password')
        db.session.add(u)
        db.session.commit()

        with self.client:
            self.client.post('/auth/login', data={'username': 'test_mf_empty', 'password': 'password'})
            
            d = Deck(name='Test Deck MF Empty', user=u)
            db.session.add(d)
            db.session.commit()

            response = self.client.get(f'/deck/{d.id}/memory-flip')
            self.assertEqual(response.status_code, 302)
            self.assertIn(f'/deck/{d.id}', response.headers.get('Location', ''))

    def test_memory_flip_valid_deck_with_cards(self):
        u = User(username='test_mf_valid', email='test_mf_valid@example.com')
        u.set_password('password')
        db.session.add(u)
        db.session.commit()

        with self.client:
            self.client.post('/auth/login', data={'username': 'test_mf_valid', 'password': 'password'})
            
            d = Deck(name='Test Deck MF Valid', user=u)
            db.session.add(d)
            db.session.commit()

            c1 = Card(word='Apple', meaning='Elma', example_sentence='I eat an apple.', deck=d)
            c2 = Card(word='Book', meaning='Kitap', example_sentence='Read a book.', deck=d)
            db.session.add_all([c1, c2])
            db.session.commit()

            response = self.client.get(f'/deck/{d.id}/memory-flip')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Apple', response.data)
            self.assertIn(b'Book', response.data)

    def test_fill_blanks_route_requires_login(self):
        response = self.client.get('/deck/1/fill-blanks')
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.headers.get('Location', '').lower())

    def test_fill_blanks_empty_deck_redirects(self):
        u = User(username='test_fb_empty', email='test_fb_empty@example.com')
        u.set_password('password')
        db.session.add(u)
        db.session.commit()

        with self.client:
            self.client.post('/auth/login', data={'username': 'test_fb_empty', 'password': 'password'})
            
            d = Deck(name='Test Deck FB Empty', user=u)
            db.session.add(d)
            db.session.commit()

            response = self.client.get(f'/deck/{d.id}/fill-blanks')
            self.assertEqual(response.status_code, 302)
            self.assertIn(f'/deck/{d.id}', response.headers.get('Location', ''))

    def test_fill_blanks_valid_deck_with_cards(self):
        u = User(username='test_fb_valid', email='test_fb_valid@example.com')
        u.set_password('password')
        db.session.add(u)
        db.session.commit()

        with self.client:
            self.client.post('/auth/login', data={'username': 'test_fb_valid', 'password': 'password'})
            
            d = Deck(name='Test Deck FB Valid', user=u)
            db.session.add(d)
            db.session.commit()

            c1 = Card(word='Apple', meaning='Elma', example_sentence='I eat an apple.', deck=d)
            c2 = Card(word='Book', meaning='Kitap', example_sentence='Read a book.', deck=d)
            db.session.add_all([c1, c2])
            db.session.commit()

            response = self.client.get(f'/deck/{d.id}/fill-blanks')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Apple', response.data)
            self.assertIn(b'Book', response.data)

if __name__ == '__main__':
    unittest.main()
