from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, Team, Activity, Leaderboard, Workout

class OctofitTrackerTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="testuser", email="testuser@example.com", password="password123")
        self.team = Team.objects.create(name="Test Team")
        self.activity = Activity.objects.create(user=self.user, activity_type="Running", duration="00:30:00")
        self.leaderboard = Leaderboard.objects.create(user=self.user, score=100)
        self.workout = Workout.objects.create(name="Morning Run", description="A quick morning run.")

    def test_user_creation(self):
        response = self.client.post('/api/users/', {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword123'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_team_creation(self):
        response = self.client.post('/api/teams/', {
            'name': 'New Team',
            'members': [self.user._id]
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_activity_creation(self):
        response = self.client.post('/api/activities/', {
            'user': self.user._id,
            'activity_type': 'Cycling',
            'duration': '01:00:00'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_leaderboard_creation(self):
        response = self.client.post('/api/leaderboard/', {
            'user': self.user._id,
            'score': 200
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_workout_creation(self):
        response = self.client.post('/api/workouts/', {
            'name': 'Evening Yoga',
            'description': 'A relaxing yoga session.'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)