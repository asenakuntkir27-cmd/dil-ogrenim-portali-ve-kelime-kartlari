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

    def test_analytics_route_requires_login(self):
        # Accessing analytics unauthenticated should redirect to login page
        response = self.client.get('/analytics')
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.headers.get('Location', '').lower())

    def test_analytics_valid_load(self):
        # Create user, login, and check successful analytics load
        u = User(username='test_analytics', email='analytics@example.com')
        u.set_password('password')
        db.session.add(u)
        db.session.commit()

        with self.client:
            self.client.post('/auth/login', data={'username': 'test_analytics', 'password': 'password'})
            
            # Create a deck and card to have real data
            d = Deck(name='İngilizce - Colors', user=u)
            db.session.add(d)
            db.session.commit()
            
            c = Card(word='Red', meaning='Kırmızı', deck=d)
            db.session.add(c)
            db.session.commit()

            response = self.client.get('/analytics')
            self.assertEqual(response.status_code, 200)
            self.assertIn('A Harfi Destesi'.encode('utf-8'), response.data) # Should render a seeded deck name
            self.assertIn(b'Haftal\xc4\xb1k \xc3\x87al\xc4\xb1\xc5\x9fma', response.data) # Haftalık Çalışma in utf-8
            self.assertIn(b'Ayl\xc4\xb1k \xc4\xb0lerleme', response.data) # Aylık İlerleme in utf-8
            self.assertIn(b'Destelere G\xc3\xb6re Da\xc4\x9f\xc4\xb1l\xc4\xb1m', response.data) # Destelere Göre Dağılım in utf-8

    def test_delete_deck_requires_login(self):
        # Accessing delete deck route unauthenticated should redirect to login page
        response = self.client.post('/deck/1/delete')
        self.assertEqual(response.status_code, 302)

    def test_delete_deck_owner_check(self):
        # Create two users
        u1 = User(username='user1', email='u1@example.com')
        u1.set_password('password')
        u2 = User(username='user2', email='u2@example.com')
        u2.set_password('password')
        db.session.add_all([u1, u2])
        db.session.commit()

        # u1 creates a deck
        d = Deck(name='User 1 Deck', user=u1)
        db.session.add(d)
        db.session.commit()

        # u2 logs in and tries to delete u1's deck
        with self.client:
            self.client.post('/auth/login', data={'username': 'user2', 'password': 'password'})
            response = self.client.post(f'/deck/{d.id}/delete')
            # Should raise 404
            self.assertEqual(response.status_code, 404)
            # Verify deck is NOT deleted
            self.assertIsNotNone(db.session.get(Deck, d.id))

    def test_delete_deck_cascades_cards(self):
        # Create user, login, deck, cards
        u = User(username='user_delete', email='ud@example.com')
        u.set_password('password')
        db.session.add(u)
        db.session.commit()

        with self.client:
            self.client.post('/auth/login', data={'username': 'user_delete', 'password': 'password'})
            d = Deck(name='Deletable Deck', user=u)
            db.session.add(d)
            db.session.commit()

            c1 = Card(word='Elma', meaning='Apple', deck=d)
            c2 = Card(word='Armut', meaning='Pear', deck=d)
            db.session.add_all([c1, c2])
            db.session.commit()

            # Verify deck and cards are in db
            self.assertIsNotNone(db.session.get(Deck, d.id))
            self.assertIsNotNone(db.session.get(Card, c1.id))
            self.assertIsNotNone(db.session.get(Card, c2.id))

            # Delete the deck
            response = self.client.post(f'/deck/{d.id}/delete')
            self.assertEqual(response.status_code, 302) # Redirects to index

            # Verify deck and cards are deleted (cascade)
            self.assertIsNone(db.session.get(Deck, d.id))
            self.assertIsNone(db.session.get(Card, c1.id))
            self.assertIsNone(db.session.get(Card, c2.id))

if __name__ == '__main__':
    unittest.main()
