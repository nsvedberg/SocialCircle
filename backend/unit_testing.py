import unittest
import json
from app import app
from app.db.session import Session
from app.db.models import Club, Event, User

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        # Set up the test client and the database session
        self.app = app.test_client()
        self.app.config['TESTING'] = True
        self.session = Session()

    def tearDown(self):
        # Clean up the database after each test
        self.session.close()

    def test_create_club(self):
        response = self.app.post('/b/clubs/new', json={
            'club_name': 'Test Club',
            'club_description': 'This is a test club.'
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('id', data)

    def test_get_all_clubs(self):
        response = self.app.get('/b/clubs')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_club_by_name(self):
        # First, create a club to fetch
        self.app.post('/b/clubs/new', json={
            'club_name': 'Unique Club',
            'club_description': 'Description for unique club.'
        })
        response = self.app.get('/b/clubs/name/Unique Club')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['club_name'], 'Unique Club')

    def test_update_club(self):
        # First, create a club to update
        create_response = self.app.post('/b/clubs/new', json={
            'club_name': 'Club to Update',
            'club_description': 'Original description.'
        })
        club_id = json.loads(create_response.data)['id']

        # Update the club
        response = self.app.put(f'/b/clubs/{club_id}', json={
            'club_name': 'Updated Club',
            'club_description': 'Updated description.',
            'club_president': 'President Name',
            'club_email': 'president@club.com',
            'club_tags': ['tag1', 'tag2'],
            'club_members': 5
        })
        self.assertEqual(response.status_code, 200)
        updated_club = json.loads(response.data)
        self.assertEqual(updated_club['club_name'], 'Updated Club')

    def test_delete_club(self):
        # First, create a club to delete
        create_response = self.app.post('/b/clubs/new', json={
            'club_name': 'Club to Delete',
            'club_description': 'This club will be deleted.'
        })
        club_id = json.loads(create_response.data)['id']

        # Delete the club
        response = self.app.delete(f'/b/clubs/{club_id}')
        self.assertEqual(response.status_code, 200)
        deleted_club = json.loads(response.data)
        self.assertEqual(deleted_club['id'], club_id)

    def test_create_event(self):
        response = self.app.post('/b/events/new', json={
            'event_name': 'Test Event',
            'event_description': 'This is a test event.',
            'event_date': '2024-11-01',
            'event_time': '12:00',
            'event_location': 'Test Location',
            'event_club': 'Test Club',
            'event_tags': ['tag1', 'tag2']
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('id', data)

    def test_create_user(self):
        response = self.app.post('/b/users/new', json={
            'user_name': 'Test User',
            'user_email': 'testuser@example.com',
            'user_clubs': ['Test Club'],
            'user_interests': ['Coding']
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('id', data)

    def test_login(self):
        # First, create a user to log in
        self.app.post('/b/users/new', json={
            'user_name': 'Login User',
            'user_email': 'loginuser@example.com',
            'user_clubs': [],
            'user_interests': []
        })
        # Here, use the correct password field when implementing User creation
        response = self.app.post('/b/login', json={
            'email': 'loginuser@example.com',
            'password': 'password'  # Ensure to adjust this to the password mechanism you have
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('data', data)  # Expecting a token

if __name__ == '__main__':
    unittest.main()
