from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from notifications.services import NotificationService
from notifications.constants import NotificationTypes

from .validators import validate_github_url, validate_linkedin_url, validate_twitter_url, validate_facebook_url, validate_leetcode_url, validate_hackerrank_url, validate_medium_url, validate_stackoverflow_url, validate_portfolio_url, validate_youtube_url, validate_devto_url


class UserSessionManager(models.Manager):
    """Custom manager for UserSession model."""

    def active(self):
        """Return only active sessions."""
        return self.filter(is_active=True)

    def expired(self):
        """Return expired sessions."""
        return self.filter(expires_at__lt=timezone.now())

    def cleanup_expired(self):
        """Terminate all expired sessions."""
        expired = self.expired()
        count = expired.count()
        expired.update(is_active=False)
        return count

    def terminate_all_except(self, session_key):
        """Terminate all sessions except the specified one."""
        return self.exclude(session_key=session_key).update(is_active=False)

    def get_user_active_sessions(self, user):
        """Get all active sessions for a user."""
        return self.active().filter(user=user).order_by('-last_activity')


# Create your models here.

class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='users')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}"

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['-created_at']),
        ]


class Profile(models.Model):
    users = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='profile')
    is_available = models.BooleanField(
        default=True,
        verbose_name=_('Availability Status'),
        help_text=_('Controls whether the badge is displayed')
    )
    badge = models.CharField(max_length=100, default="", blank=True)
    name = models.CharField(max_length=100, default="", blank=True)
    title = models.CharField(max_length=100, default="", blank=True)
    description = models.TextField(default="", blank=True)
    
    # Social Links
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
    if created:
        users = Users.objects.create(user=instance)
        Profile.objects.create(users=users)


class UserSession(models.Model):
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

    class Meta:
        ordering = ['-last_activity']
        indexes = [
            models.Index(fields=['user', '-last_activity']),
            models.Index(fields=['session_key']),
            models.Index(fields=['is_active']),
        ]

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(minutes=30)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() >= self.expires_at

    def extend_session(self, hours=24):
        self.expires_at = timezone.now() + timezone.timedelta(hours=hours)
        self.save()

    def terminate(self):
        self.is_active = False
        self.save()
        NotificationService.create_notification(
            recipient=self.user,
            notification_type=NotificationTypes.SESSION_TERMINATED,
            message=f"Session from {self.device_type or 'unknown device'} was terminated",
            content_object=self,
            extra_data={
                'session_id': self.id,
                'ip_address': self.ip_address,
                'location': self.location,
                'device_type': self.device_type
            }
        )
