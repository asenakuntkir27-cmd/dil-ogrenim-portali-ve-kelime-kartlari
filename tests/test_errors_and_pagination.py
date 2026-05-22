import unittest
from app import create_app, db
from app.models import User, Deck
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False

class ErrorsAndPaginationTestCase(unittest.TestCase):
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

    def test_custom_404_page(self):
        # Accessing an invalid route should return 404 and render our custom template
        response = self.client.get('/invalid-route-that-does-not-exist')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'404 - Sayfa Bulunamad', response.data)
        self.assertIn(b'Ana Sayfaya D', response.data)

    def test_deck_pagination(self):
        # Create a user
        u = User(username='testuser', email='testuser@example.com')
        u.set_password('password')
        db.session.add(u)
        db.session.commit()

        # Log the user in
        self.client.post('/auth/login', data={'username': 'testuser', 'password': 'password'})

        # Create 12 decks with distinct created_at times to guarantee descending order sorting
        from datetime import datetime, timezone, timedelta
        base_time = datetime.now(timezone.utc)
        for i in range(1, 13):
            d = Deck(
                name=f'Deste {i:02d}',
                description=f'Aciklama {i:02d}',
                user=u,
                created_at=base_time + timedelta(minutes=i)
            )
            db.session.add(d)
        db.session.commit()

        # Get index page (page 1)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        # Decks are sorted by created_at desc, so Deste 12 down to Deste 03 should be on page 1
        # and Deste 02, Deste 01 should be on page 2.
        self.assertIn(b'Deste 12', response.data)
        self.assertIn(b'Deste 03', response.data)
        self.assertNotIn(b'Deste 02', response.data)
        self.assertNotIn(b'Deste 01', response.data)

        # Verify page 2 links and info text are visible
        self.assertIn(b'Toplam <span class="font-semibold text-zinc-300">12</span> deste', response.data)
        self.assertIn(b'sayfa <span class="font-semibold text-zinc-300">1</span> / <span class="font-semibold text-zinc-300">2</span>', response.data)

        # Fetch page 2
        response_page2 = self.client.get('/?page=2')
        self.assertEqual(response_page2.status_code, 200)
        self.assertIn(b'Deste 02', response_page2.data)
        self.assertIn(b'Deste 01', response_page2.data)
        self.assertNotIn(b'Deste 12', response_page2.data)

if __name__ == '__main__':
    unittest.main()
