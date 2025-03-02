# Create your tests here.

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError

from .models import Users, Profile, UserSession
from .serializers import UserSerializer, ProfileSerializer, UserSessionSerializer
from .constants import UserConstants
from .validators import validate_github_url, validate_linkedin_url, validate_portfolio_url


class UserModelTest(TestCase):
    """Test cases for User-related models."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )

    def test_users_creation(self):
        """Test that Users and Profile are created automatically."""
        self.assertTrue(hasattr(self.user, 'users'))
        self.assertTrue(hasattr(self.user.users, 'profile'))
        self.assertIsInstance(self.user.users, Users)
        self.assertIsInstance(self.user.users.profile, Profile)

    def test_profile_defaults(self):
        """Test that Profile fields have correct default values."""
        profile = self.user.users.profile
        self.assertTrue(profile.is_available)
        self.assertEqual(profile.badge, '')
        self.assertEqual(profile.name, '')
        self.assertEqual(profile.title, '')
        self.assertEqual(profile.description, '')
        
        # Test social links default to None
        social_fields = [
            'github', 'linkedin', 'twitter', 'facebook', 'leetcode',
            'hackerrank', 'medium', 'stackoverflow', 'portfolio',
            'youtube', 'devto'
        ]
        for field in social_fields:
            self.assertIsNone(getattr(profile, field))

    def test_string_representation(self):
        """Test string representation of models."""
        self.assertEqual(str(self.user.users), 'testuser')
        self.assertEqual(str(self.user.users.profile), "testuser's profile")


class UserSessionTest(TestCase):
    """Test cases for UserSession model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.session = UserSession.objects.create(
            user=self.user,
            session_key='test_session',
            expires_at=timezone.now() + timezone.timedelta(minutes=30)
        )

    def test_session_expiry(self):
        """Test session expiry functionality."""
        # Test active session
        self.assertFalse(self.session.is_expired())
        
        # Test expired session
        self.session.expires_at = timezone.now() - timezone.timedelta(minutes=1)
        self.session.save()
        self.assertTrue(self.session.is_expired())

    def test_session_extension(self):
        """Test session extension functionality."""
        old_expiry = self.session.expires_at
        self.session.extend_session(hours=2)
        self.assertGreater(self.session.expires_at, old_expiry)

    def test_session_termination(self):
        """Test session termination functionality."""
        self.assertTrue(self.session.is_active)
        self.session.terminate()
        self.assertFalse(self.session.is_active)


class UserAPITest(APITestCase):
    """Test cases for User-related API endpoints."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.client.force_authenticate(user=self.user)

    def test_get_profile(self):
        """Test retrieving user profile."""
        url = reverse('user-profile', kwargs={'username': self.user.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_update_profile(self):
        """Test updating user profile."""
        url = reverse('user-profile', kwargs={'username': self.user.username})
        data = {
            'users': {
                'profile': {
                    'title': 'Software Engineer',
                    'name': 'Test User',
                    'description': 'Test Description',
                    'github': 'https://github.com/testuser'
                }
            }
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify updates
        self.user.refresh_from_db()
        profile = self.user.users.profile
        self.assertEqual(profile.title, 'Software Engineer')
        self.assertEqual(profile.name, 'Test User')
        self.assertEqual(profile.description, 'Test Description')
        self.assertEqual(profile.github, 'https://github.com/testuser')

    def test_create_user(self):
        """Test user creation endpoint."""
        url = reverse('user-create')
        data = {
            'username': 'newuser',
            'password': 'NewPass123!',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'users': {
                'profile': {
                    'title': 'Software Developer',
                    'name': 'New User',
                    'description': 'New user description',
                    'github': 'https://github.com/newuser'
                }
            }
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify user creation
        user = User.objects.get(username='newuser')
        self.assertEqual(user.email, 'newuser@example.com')
        self.assertEqual(user.first_name, 'New')
        self.assertEqual(user.users.profile.title, 'Software Developer')
        self.assertEqual(user.users.profile.github, 'https://github.com/newuser')

    def test_invalid_profile_update(self):
        """Test profile update with invalid data."""
        url = reverse('user-profile', kwargs={'username': self.user.username})
        data = {
            'users': {
                'profile': {
                    'github': 'invalid-url'  # Invalid GitHub URL
                }
            }
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserSerializerTest(TestCase):
    """Test cases for User-related serializers."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        self.profile = self.user.users.profile
        self.profile.title = 'Software Engineer'
        self.profile.github = 'https://github.com/testuser'
        self.profile.save()

    def test_user_serializer(self):
        """Test UserSerializer functionality."""
        serializer = UserSerializer(self.user)
        data = serializer.data
        
        # Test basic user fields
        self.assertEqual(data['username'], 'testuser')
        self.assertEqual(data['email'], 'test@example.com')
        self.assertEqual(data['first_name'], 'Test')
        
        # Test nested profile data
        profile_data = data['users']['profile']
        self.assertEqual(profile_data['title'], 'Software Engineer')
        self.assertEqual(profile_data['github'], 'https://github.com/testuser')

    def test_profile_serializer(self):
        """Test ProfileSerializer functionality."""
        serializer = ProfileSerializer(self.profile)
        data = serializer.data
        
        self.assertEqual(data['title'], 'Software Engineer')
        self.assertEqual(data['github'], 'https://github.com/testuser')
        self.assertTrue('is_available' in data)

    def test_user_session_serializer(self):
        """Test UserSessionSerializer functionality."""
        session = UserSession.objects.create(
            user=self.user,
            session_key='test_session',
            expires_at=timezone.now() + timezone.timedelta(minutes=30)
        )
        serializer = UserSessionSerializer(session)
        data = serializer.data
        
        self.assertEqual(data['session_key'], 'test_session')
        self.assertTrue('duration' in data)
        self.assertTrue('time_until_expiry' in data)


class URLValidatorTest(TestCase):
    """Test cases for URL validators."""

    def test_github_url_validation(self):
        """Test GitHub URL validation."""
        # Valid URLs
        valid_urls = [
            'https://github.com/username',
            'http://github.com/user-name',
            'https://www.github.com/user123',
            'http://www.github.com/user_name'
        ]
        for url in valid_urls:
            try:
                validate_github_url(url)
            except ValidationError:
                self.fail(f"Valid GitHub URL {url} failed validation")

        # Invalid URLs
        invalid_urls = [
            'http://githubs.com/username',
            'https://github.com/user/repo',
            'https://github.com/',
            'github.com/username',
            'https://github.com/user@name',
            'https://github.com/user name'
        ]
        for url in invalid_urls:
            with self.assertRaises(ValidationError):
                validate_github_url(url)

    def test_linkedin_url_validation(self):
        """Test LinkedIn URL validation."""
        # Valid URLs
        valid_urls = [
            'https://linkedin.com/in/username',
            'http://linkedin.com/in/user-name',
            'https://www.linkedin.com/in/user123',
            'http://www.linkedin.com/in/user_name'
        ]
        for url in valid_urls:
            try:
                validate_linkedin_url(url)
            except ValidationError:
                self.fail(f"Valid LinkedIn URL {url} failed validation")

        # Invalid URLs
        invalid_urls = [
            'http://linkedins.com/in/username',
            'https://linkedin.com/profile/username',
            'https://linkedin.com/',
            'linkedin.com/in/username',
            'https://linkedin.com/in/user@name',
            'https://linkedin.com/in/user name'
        ]
        for url in invalid_urls:
            with self.assertRaises(ValidationError):
                validate_linkedin_url(url)

    def test_portfolio_url_validation(self):
        """Test portfolio URL validation."""
        # Valid URLs
        valid_urls = [
            'https://example.com',
            'http://subdomain.example.com',
            'https://my-portfolio.dev',
            'http://www.example.com/portfolio',
            'https://example.com/about'
        ]
        for url in valid_urls:
            try:
                validate_portfolio_url(url)
            except ValidationError:
                self.fail(f"Valid portfolio URL {url} failed validation")

        # Invalid URLs
        invalid_urls = [
            'not-a-url',
            'ftp://example.com',
            'example.com',
            'https://.com',
            'https://example.'
        ]
        for url in invalid_urls:
            with self.assertRaises(ValidationError):
                validate_portfolio_url(url)

    def test_empty_and_none_values(self):
        """Test that empty and None values are allowed."""
        # Validators
        validators = [
            validate_github_url,
            validate_linkedin_url,
            validate_portfolio_url
        ]

        for validator in validators:
            try:
                validator(None)
                validator('')
            except ValidationError:
                self.fail(f"Validator {validator.__name__} failed for empty/None value")


class UserSessionManagerTest(TestCase):
    """Test cases for user session management."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_multiple_sessions(self):
        """Test handling of multiple sessions for a user."""
        # Create multiple sessions
        sessions = []
        for i in range(3):
            session = UserSession.objects.create(
                user=self.user,
                session_key=f'test_session_{i}',
                expires_at=timezone.now() + timezone.timedelta(minutes=30)
            )
            sessions.append(session)

        # Verify all sessions are active
        active_sessions = UserSession.objects.filter(
            user=self.user,
            is_active=True
        )
        self.assertEqual(active_sessions.count(), 3)

        # Terminate one session
        sessions[0].terminate()
        active_sessions = UserSession.objects.filter(
            user=self.user,
            is_active=True
        )
        self.assertEqual(active_sessions.count(), 2)

    def test_session_cleanup(self):
        """Test cleanup of expired sessions."""
        # Create expired and active sessions
        expired_session = UserSession.objects.create(
            user=self.user,
            session_key='expired_session',
            expires_at=timezone.now() - timezone.timedelta(minutes=1)
        )
        active_session = UserSession.objects.create(
            user=self.user,
            session_key='active_session',
            expires_at=timezone.now() + timezone.timedelta(minutes=30)
        )

        # Verify expired session is marked as expired
        self.assertTrue(expired_session.is_expired())
        self.assertFalse(active_session.is_expired())

    def test_session_extension(self):
        """Test session extension with different durations."""
        session = UserSession.objects.create(
            user=self.user,
            session_key='test_session',
            expires_at=timezone.now() + timezone.timedelta(minutes=30)
        )

        # Test different extension durations
        durations = [1, 24, 168]  # hours
        for hours in durations:
            old_expiry = session.expires_at
            session.extend_session(hours=hours)
            expected_expiry = old_expiry + timezone.timedelta(hours=hours)
            self.assertGreater(session.expires_at, old_expiry)
            self.assertEqual(
                session.expires_at.replace(microsecond=0),
                expected_expiry.replace(microsecond=0)
            )


class UserAuthenticationTest(APITestCase):
    """Test cases for user authentication."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )

    def test_login_with_email(self):
        """Test login using email instead of username."""
        url = reverse('login')
        data = {
            'username_or_email': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_with_invalid_credentials(self):
        """Test login with invalid credentials."""
        url = reverse('login')
        invalid_data = [
            {'username_or_email': 'test@example.com', 'password': 'wrongpass'},
            {'username_or_email': 'wrong@example.com', 'password': 'testpass123'},
            {'username_or_email': '', 'password': 'testpass123'},
            {'username_or_email': 'test@example.com', 'password': ''}
        ]
        for data in invalid_data:
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_refresh(self):
        """Test token refresh functionality."""
        # First login to get tokens
        login_url = reverse('login')
        login_data = {
            'username_or_email': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(login_url, login_data, format='json')
        refresh_token = response.data['refresh']

        # Try to refresh token
        refresh_url = reverse('token-refresh')
        refresh_data = {'refresh': refresh_token}
        response = self.client.post(refresh_url, refresh_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_logout(self):
        """Test logout functionality."""
        # First login
        login_url = reverse('login')
        login_data = {
            'username_or_email': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(login_url, login_data, format='json')
        refresh_token = response.data['refresh']
        access_token = response.data['access']

        # Then logout
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        logout_url = reverse('logout')
        logout_data = {'refresh_token': refresh_token}
        response = self.client.post(logout_url, logout_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify token is blacklisted by trying to refresh
        refresh_url = reverse('token-refresh')
        refresh_data = {'refresh': refresh_token}
        response = self.client.post(refresh_url, refresh_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
