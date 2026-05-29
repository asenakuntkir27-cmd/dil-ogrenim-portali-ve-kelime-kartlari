import unittest
from app import create_app, db
from config import Config
from app.models import User, Score

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False

class LeaderboardTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # Create two test users
        self.u1 = User(username='player1', email='p1@example.com')
        self.u1.set_password('pass')
        self.u2 = User(username='player2', email='p2@example.com')
        self.u2.set_password('pass')
        db.session.add_all([self.u1, self.u2])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_submit_requires_login(self):
        # Submission without login should redirect/fail
        response = self.client.post('/api/v1/scores/submit', json={
            'game_name': 'Kelime Tetrisi',
            'score': 100
        })
        self.assertEqual(response.status_code, 302)

    def test_submit_invalid_payload(self):
        with self.client:
            self.client.post('/auth/login', data={'username': 'player1', 'password': 'pass'})

            # Invalid game name
            response = self.client.post('/api/v1/scores/submit', json={
                'game_name': 'Super Mario',
                'score': 100
            })
            self.assertEqual(response.status_code, 400)
            self.assertFalse(response.json['success'])

            # Negative score
            response2 = self.client.post('/api/v1/scores/submit', json={
                'game_name': 'Kelime Tetrisi',
                'score': -50
            })
            self.assertEqual(response2.status_code, 400)

            # Non-integer score
            response3 = self.client.post('/api/v1/scores/submit', json={
                'game_name': 'Kelime Tetrisi',
                'score': 'not-an-int'
            })
            self.assertEqual(response3.status_code, 400)

    def test_submit_valid_score(self):
        with self.client:
            self.client.post('/auth/login', data={'username': 'player1', 'password': 'pass'})

            response = self.client.post('/api/v1/scores/submit', json={
                'game_name': 'Kelime Tetrisi',
                'score': 150
            })
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.json['success'])

            # Verify in db
            scores = db.session.scalars(db.select(Score).where(Score.user_id == self.u1.id)).all()
            self.assertEqual(len(scores), 1)
            self.assertEqual(scores[0].game_name, 'Kelime Tetrisi')
            self.assertEqual(scores[0].score, 150)

    def test_leaderboard_sorting_and_limits(self):
        # Create multiple scores for 'Cümle Kurma'
        # Player 1 scores: 50, 100, 150
        # Player 2 scores: 80, 200, 120, 30
        scores_list = [
            Score(user_id=self.u1.id, game_name='Cümle Kurma', score=50),
            Score(user_id=self.u1.id, game_name='Cümle Kurma', score=100),
            Score(user_id=self.u1.id, game_name='Cümle Kurma', score=150),
            Score(user_id=self.u2.id, game_name='Cümle Kurma', score=80),
            Score(user_id=self.u2.id, game_name='Cümle Kurma', score=200),
            Score(user_id=self.u2.id, game_name='Cümle Kurma', score=120),
            Score(user_id=self.u2.id, game_name='Cümle Kurma', score=30),
        ]
        db.session.add_all(scores_list)
        db.session.commit()

        # Call leaderboard API
        response = self.client.get('/api/v1/scores/leaderboard')
        self.assertEqual(response.status_code, 200)
        data = response.json

        # 'Cümle Kurma' list should have max 5 items
        ck_leaderboard = data.get('Cümle Kurma', [])
        self.assertEqual(len(ck_leaderboard), 5)

        # Checking sorting order (200, 150, 120, 100, 80)
        scores_received = [x['score'] for x in ck_leaderboard]
        self.assertEqual(scores_received, [200, 150, 120, 100, 80])

        # Check players matching
        self.assertEqual(ck_leaderboard[0]['username'], 'player2') # 200 by player2
        self.assertEqual(ck_leaderboard[1]['username'], 'player1') # 150 by player1

        # Check empty game lists in leaderboard
        self.assertEqual(data.get('Kelime Tetrisi'), [])

if __name__ == '__main__':
    unittest.main()
