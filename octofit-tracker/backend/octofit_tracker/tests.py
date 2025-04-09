from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from .models import User, Team, Activity, Leaderboard, Workout
from datetime import timedelta

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

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create(username="testuser", email="testuser@example.com", password="password123")
        self.assertEqual(user.username, "testuser")

class TeamModelTest(TestCase):
    def test_create_team(self):
        user = User.objects.create(username="testuser", email="testuser@example.com", password="password123")
        team = Team.objects.create(name="Test Team")
        team.members.add(user)
        self.assertEqual(team.name, "Test Team")

class ActivityModelTest(TestCase):
    def test_create_activity(self):
        user = User.objects.create(username="testuser", email="testuser@example.com", password="password123")
        activity = Activity.objects.create(user=user, activity_type="Running", duration="01:00:00")
        self.assertEqual(activity.activity_type, "Running")

class LeaderboardModelTest(TestCase):
    def test_create_leaderboard_entry(self):
        user = User.objects.create(username="testuser", email="testuser@example.com", password="password123")
        leaderboard = Leaderboard.objects.create(user=user, score=100)
        self.assertEqual(leaderboard.score, 100)

class WorkoutModelTest(TestCase):
    def test_create_workout(self):
        workout = Workout.objects.create(name="Test Workout", description="Test Description")
        self.assertEqual(workout.name, "Test Workout")

class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        self.team = Team.objects.create(name="Test Team")
        self.workout = Workout.objects.create(
            name="Test Workout",
            description="Test workout description"
        )
        self.activity = Activity.objects.create(
            user=self.user,
            activity_type="running",
            duration=timedelta(minutes=30)
        )
        self.leaderboard = Leaderboard.objects.create(
            user=self.user,
            score=100
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "test@example.com")

    def test_team_creation(self):
        self.assertEqual(self.team.name, "Test Team")

    def test_activity_creation(self):
        self.assertEqual(self.activity.activity_type, "running")
        self.assertEqual(self.activity.duration, timedelta(minutes=30))

    def test_leaderboard_creation(self):
        self.assertEqual(self.leaderboard.score, 100)

    def test_workout_creation(self):
        self.assertEqual(self.workout.name, "Test Workout")
        self.assertEqual(self.workout.description, "Test workout description")

class APITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        self.team = Team.objects.create(name="Test Team")

    def test_user_list(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_team_list(self):
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_activity(self):
        data = {
            'user': self.user.id,
            'activity_type': 'running',
            'duration': '00:30:00'
        }
        response = self.client.post('/api/activities/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_workout(self):
        data = {
            'name': 'New Workout',
            'description': 'New workout description'
        }
        response = self.client.post('/api/workouts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)