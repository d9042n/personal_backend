from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from notifications.services import NotificationService
from notifications.constants import NotificationTypes
import logging

from .constants import UserConstants
from .validators import (
    validate_github_url, validate_linkedin_url, validate_twitter_url,
    validate_facebook_url, validate_leetcode_url, validate_hackerrank_url,
    validate_medium_url, validate_stackoverflow_url, validate_portfolio_url,
    validate_youtube_url, validate_devto_url
)

logger = logging.getLogger(__name__)

class UserSessionManager(models.Manager):
    """Manager for handling UserSession operations."""

    def active(self):
        """Return only active sessions."""
        return self.filter(is_active=True)

    def expired(self):
        """Return expired sessions."""
        return self.filter(expires_at__lt=timezone.now())

    def cleanup_expired(self):
        """Terminate all expired sessions and return count of terminated sessions."""
        expired = self.expired()
        count = expired.count()
        if count > 0:
            logger.info(f"Cleaning up {count} expired sessions")
            expired.update(is_active=False)
        return count

    def terminate_all_except(self, session_key):
        """
        Terminate all sessions except the specified one.
        
        Args:
            session_key (str): The session key to preserve
            
        Returns:
            int: Number of sessions terminated
        """
        terminated = self.exclude(session_key=session_key).update(is_active=False)
        if terminated > 0:
            logger.info(f"Terminated {terminated} sessions (preserving {session_key})")
        return terminated

    def get_user_active_sessions(self, user):
        """
        Get all active sessions for a user.
        
        Args:
            user (User): The user whose sessions to retrieve
            
        Returns:
            QuerySet: Active sessions ordered by last activity
        """
        return self.active().filter(user=user).order_by('-last_activity')


class Users(models.Model):
    """
    Extended user profile model that maintains a one-to-one relationship with Django's User model.
    This model stores additional user-specific data not covered by the default User model.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='users')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        """Override save to add logging"""
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new:
            logger.info(f"Created new Users instance for user: {self.user.username}")
        else:
            logger.debug(f"Updated Users instance for user: {self.user.username}")

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['-created_at']),
        ]


class Profile(models.Model):
    """
    User profile model storing extended profile information and social media links.
    Each profile is associated with exactly one Users instance.
    """
    users = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='profile')
    
    # Availability status
    is_available = models.BooleanField(
        default=True,
        verbose_name=_('Availability Status'),
        help_text=_('Controls whether the badge is displayed')
    )
    
    # Profile badge shown on user's profile
    badge = models.CharField(
        max_length=100, 
        default=UserConstants.Badges.AVAILABLE, 
        blank=True
    )
    
    # Basic profile information
    name = models.CharField(max_length=100, default="", blank=True)
    title = models.CharField(max_length=100, default=UserConstants.DEFAULT_TITLE, blank=True)
    description = models.TextField(default="", blank=True)
    
    # Social Links with validation
    github = models.URLField(null=True, blank=True, validators=[validate_github_url])
    linkedin = models.URLField(null=True, blank=True, validators=[validate_linkedin_url])
    twitter = models.URLField(null=True, blank=True, validators=[validate_twitter_url])
    facebook = models.URLField(null=True, blank=True, validators=[validate_facebook_url])
    leetcode = models.URLField(null=True, blank=True, validators=[validate_leetcode_url])
    hackerrank = models.URLField(null=True, blank=True, validators=[validate_hackerrank_url])
    medium = models.URLField(null=True, blank=True, validators=[validate_medium_url])
    stackoverflow = models.URLField(null=True, blank=True, validators=[validate_stackoverflow_url])
    portfolio = models.URLField(null=True, blank=True, validators=[validate_portfolio_url])
    youtube = models.URLField(null=True, blank=True, validators=[validate_youtube_url])
    devto = models.URLField(null=True, blank=True, validators=[validate_devto_url])

    def __str__(self):
        return f"{self.users.user.username}'s profile"

    class Meta:
        indexes = [
            models.Index(fields=['users']),
            models.Index(fields=['badge']),
            models.Index(fields=['is_available']),
        ]


@receiver(post_save, sender=User)
def create_users(sender, instance, created, **kwargs):
    """
    Signal handler to automatically create Users and Profile instances when a new User is created.
    
    Args:
        sender: The model class (User)
        instance: The actual instance being saved
        created: Boolean; True if a new record was created
        **kwargs: Additional keyword arguments
    """
    if created:
        logger.info(f"Creating Users and Profile instances for new user: {instance.username}")
        try:
            users = Users.objects.create(user=instance)
            Profile.objects.create(users=users)
            logger.info(f"Successfully created Users and Profile for {instance.username}")
        except Exception as e:
            logger.error(f"Error creating Users/Profile for {instance.username}: {str(e)}", exc_info=True)
            raise


class UserSession(models.Model):
    """
    Model to track user sessions with additional metadata about the session.
    Includes information about the device, location, and session status.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    session_key = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    device_type = models.CharField(max_length=20, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField()

    objects = UserSessionManager()

    def save(self, *args, **kwargs):
        """Override save to ensure expires_at is set and add logging."""
        is_new = self._state.adding
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(minutes=30)
        
        super().save(*args, **kwargs)
        
        if is_new:
            logger.info(f"Created new session for user {self.user.username} from {self.ip_address} ({self.device_type})")
        else:
            logger.debug(f"Updated session {self.session_key} for user {self.user.username}")

    def is_expired(self):
        """Check if the session has expired."""
        is_expired = timezone.now() >= self.expires_at
        if is_expired:
            logger.info(f"Session {self.session_key} for user {self.user.username} has expired")
        return is_expired

    def extend_session(self, hours=24):
        """Extend the session expiration time."""
        self.expires_at = timezone.now() + timezone.timedelta(hours=hours)
        logger.info(f"Extended session {self.session_key} for user {self.user.username} by {hours} hours")
        self.save()

    def terminate(self):
        """Terminate the session."""
        self.is_active = False
        logger.info(f"Terminated session {self.session_key} for user {self.user.username}")
        self.save()

    class Meta:
        ordering = ['-last_activity']
        indexes = [
            models.Index(fields=['user', '-last_activity']),
            models.Index(fields=['session_key']),
            models.Index(fields=['is_active']),
        ]
