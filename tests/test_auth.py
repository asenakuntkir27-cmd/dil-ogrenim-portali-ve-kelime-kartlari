import unittest
from app import create_app, db
from app.models import User
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False

class AuthTestCase(unittest.TestCase):
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

    def test_profile_route_requires_login(self):
        # Accessing profile page unauthenticated should redirect to login page
        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.headers.get('Location', '').lower())

    def test_profile_page_renders_correctly(self):
        # Create and login user
        u = User(username='testuser', email='testuser@example.com')
        u.set_password('password123')
        db.session.add(u)
        db.session.commit()

        with self.client:
            self.client.post('/auth/login', data={'username': 'testuser', 'password': 'password123'})
            
            # Access profile page
            response = self.client.get('/profile')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'testuser', response.data)
            self.assertIn(b'testuser@example.com', response.data)
            self.assertIn(b'Profil Bilgileri', response.data)
            self.assertIn(b'G\xc3\xbcvenlik', response.data) # "Güvenlik" in utf-8
            self.assertIn(b'Gizlilik', response.data)

    def test_profile_update_success(self):
        # Create and login user
        u = User(username='olduser', email='old@example.com')
        u.set_password('password123')
        db.session.add(u)
        db.session.commit()

        with self.client:
            self.client.post('/auth/login', data={'username': 'olduser', 'password': 'password123'})
            
            # Update profile info
            response = self.client.post('/profile', data={
                'submit_type': 'profile',
                'profile-username': 'newuser',
                'profile-email': 'new@example.com'
            }, follow_redirects=True)
            
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Profil bilgileriniz ba\xc5\x9far\xc4\xb1yla g\xc3\xbcncellendi!', response.data)
            
            # Check db
            db_user = db.session.get(User, u.id)
            self.assertEqual(db_user.username, 'newuser')
            self.assertEqual(db_user.email, 'new@example.com')

    def test_profile_update_validation_duplicate_username(self):
        # Create two users
        u1 = User(username='user1', email='user1@example.com')
        u1.set_password('password123')
        u2 = User(username='user2', email='user2@example.com')
        u2.set_password('password123')
        db.session.add_all([u1, u2])
        db.session.commit()

        with self.client:
            self.client.post('/auth/login', data={'username': 'user1', 'password': 'password123'})
            
            # Try to change user1's username to user2 (duplicate)
            response = self.client.post('/profile', data={
                'submit_type': 'profile',
                'profile-username': 'user2',
                'profile-email': 'user1@example.com'
            })
            
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Bu kullan\xc4\xb1c\xc4\xb1 ad\xc4\xb1 zaten al\xc4\xb1nm\xc4\xb1\xc5\x9f', response.data)
            
            # Check db username unchanged
            db_user = db.session.get(User, u1.id)
            self.assertEqual(db_user.username, 'user1')

    def test_profile_update_validation_duplicate_email(self):
        # Create two users
        u1 = User(username='user1', email='user1@example.com')
        u1.set_password('password123')
        u2 = User(username='user2', email='user2@example.com')
        u2.set_password('password123')
        db.session.add_all([u1, u2])
        db.session.commit()

        with self.client:
            self.client.post('/auth/login', data={'username': 'user1', 'password': 'password123'})
            
            # Try to change user1's email to user2's email (duplicate)
            response = self.client.post('/profile', data={
                'submit_type': 'profile',
                'profile-username': 'user1',
                'profile-email': 'user2@example.com'
            })
            
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Bu e-posta adresi zaten kullan\xc4\xb1l\xc4\xb1yor', response.data)
            
            # Check db email unchanged
            db_user = db.session.get(User, u1.id)
            self.assertEqual(db_user.email, 'user1@example.com')

    def test_password_change_success(self):
        # Create and login user
        u = User(username='testuser', email='testuser@example.com')
        u.set_password('password123')
        db.session.add(u)
        db.session.commit()

        with self.client:
            self.client.post('/auth/login', data={'username': 'testuser', 'password': 'password123'})
            
            # Update password
            response = self.client.post('/profile', data={
                'submit_type': 'password',
                'password-current_password': 'password123',
                'password-new_password': 'newpassword',
                'password-password_confirm': 'newpassword'
            }, follow_redirects=True)
            
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'\xc5\x9eifreniz ba\xc5\x9far\xc4\xb1yla g\xc3\xbcncellendi!', response.data)
            
            # Check db password hash is updated and works
            db_user = db.session.get(User, u.id)
            self.assertTrue(db_user.check_password('newpassword'))
            self.assertFalse(db_user.check_password('password123'))

    def test_password_change_fail_wrong_current(self):
        # Create and login user
        u = User(username='testuser', email='testuser@example.com')
        u.set_password('password123')
        db.session.add(u)
        db.session.commit()

        with self.client:
            self.client.post('/auth/login', data={'username': 'testuser', 'password': 'password123'})
            
            # Update password with wrong current password
            response = self.client.post('/profile', data={
                'submit_type': 'password',
                'password-current_password': 'wrongpassword',
                'password-new_password': 'newpassword',
                'password-password_confirm': 'newpassword'
            })
            
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Mevcut \xc5\x9fifreniz yanl\xc4\xb1\xc5\x9f', response.data)
            
            # Check db password still old password
            db_user = db.session.get(User, u.id)
            self.assertTrue(db_user.check_password('password123'))

    def test_password_change_fail_mismatch(self):
        # Create and login user
        u = User(username='testuser', email='testuser@example.com')
        u.set_password('password123')
        db.session.add(u)
        db.session.commit()

        with self.client:
            self.client.post('/auth/login', data={'username': 'testuser', 'password': 'password123'})
            
            # Update password with mismatching confirm password
            response = self.client.post('/profile', data={
                'submit_type': 'password',
                'password-current_password': 'password123',
                'password-new_password': 'newpassword',
                'password-password_confirm': 'different'
            })
            
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'e\xc5\x9fle\xc5\x9fmiyor', response.data)
            
            # Check db password still old password
            db_user = db.session.get(User, u.id)
            self.assertTrue(db_user.check_password('password123'))

    def test_update_avatar_requires_login(self):
        # Unauthenticated request to /update-avatar should redirect/fail
        response = self.client.post('/update-avatar', json={'avatar_url': 'fa-robot'})
        self.assertEqual(response.status_code, 302)

    def test_update_avatar_success(self):
        # Create and login user
        u = User(username='avataruser', email='avatar@example.com')
        u.set_password('password123')
        db.session.add(u)
        db.session.commit()

        with self.client:
            self.client.post('/auth/login', data={'username': 'avataruser', 'password': 'password123'})
            
            response = self.client.post('/update-avatar', json={'avatar_url': 'fa-robot'})
            self.assertEqual(response.status_code, 200)
            
            data = response.get_json()
            self.assertTrue(data['success'])
            self.assertEqual(data['avatar_url'], 'fa-robot')
            
            # Check DB
            db_user = db.session.get(User, u.id)
            self.assertEqual(db_user.avatar_url, 'fa-robot')

    def test_update_avatar_invalid_rejected(self):
        # Create and login user
        u = User(username='avataruser2', email='avatar2@example.com')
        u.set_password('password123')
        db.session.add(u)
        db.session.commit()

        with self.client:
            self.client.post('/auth/login', data={'username': 'avataruser2', 'password': 'password123'})
            
            # Try to send a non-allowed avatar string
            response = self.client.post('/update-avatar', json={'avatar_url': 'fa-invalid-hack'})
            self.assertEqual(response.status_code, 400)
            
            data = response.get_json()
            self.assertFalse(data['success'])
            self.assertEqual(data['message'], 'Geçersiz avatar seçimi.')
            
            # Check DB is still default
            db_user = db.session.get(User, u.id)
            self.assertEqual(db_user.avatar_url, 'fa-user')
