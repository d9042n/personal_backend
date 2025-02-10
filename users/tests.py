# Create your tests here.

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Users, Profile
from .serializers import UserSerializer

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )

    def test_users_creation(self):
        """Test that Users and Profile are created automatically"""
        self.assertTrue(hasattr(self.user, 'users'))
        self.assertTrue(hasattr(self.user.users, 'profile'))
        
    def test_profile_defaults(self):
        """Test that Profile fields have correct default values"""
        profile = self.user.users.profile
        self.assertEqual(profile.badge, '')
        self.assertEqual(profile.name, '')
        self.assertEqual(profile.title, '')
        
    def test_string_representation(self):
        """Test string representation of models"""
        self.assertEqual(str(self.user.users), 'testuser')
        self.assertEqual(str(self.user.users.profile), "testuser's profile")

class UserAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.client.force_authenticate(user=self.user)
        
    def test_get_profile(self):
        """Test retrieving user profile"""
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        
    def test_update_profile(self):
        """Test updating user profile"""
        url = reverse('profile')
        data = {
            'users': {
                'profile': {
                    'title': 'Software Engineer',
                    'name': 'Test User'
                }
            }
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.users.profile.title, 'Software Engineer')
        
    def test_create_user(self):
        """Test user creation endpoint"""
        url = reverse('user-list-create')
        data = {
            'username': 'testuser123',
            'password': 'TestPass123!',
            'email': 'test@example.com',
            'users': {
                'profile': {
                    'title': 'Software Developer',
                    'name': 'Test User',
                    'description': 'Test user description'
                }
            }
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser123').exists())

class UserSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
    def test_serializer_contains_expected_fields(self):
        """Test that serializer includes all expected fields"""
        serializer = UserSerializer(self.user)
        expected_fields = {'id', 'username', 'email', 'first_name', 'last_name', 'users'}
        self.assertEqual(set(serializer.data.keys()), expected_fields)
