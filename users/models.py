from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .validators import validate_github_url, validate_linkedin_url, validate_twitter_url


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
    badge = models.CharField(max_length=100, default="", blank=True)
    name = models.CharField(max_length=100, default="", blank=True)
    title = models.CharField(max_length=100, default="", blank=True)
    description = models.TextField(default="", blank=True)
    github = models.URLField(null=True, blank=True, validators=[validate_github_url])
    linkedin = models.URLField(null=True, blank=True, validators=[validate_linkedin_url])
    twitter = models.URLField(null=True, blank=True, validators=[validate_twitter_url])

    def __str__(self):
        return f"{self.users.user.username}'s profile"

    class Meta:
        indexes = [
            models.Index(fields=['users']),
            models.Index(fields=['badge']),
        ]


@receiver(post_save, sender=User)
def create_users(sender, instance, created, **kwargs):
    if created:
        users = Users.objects.create(user=instance)
        Profile.objects.create(users=users)


@receiver(post_save, sender=User)
def save_users(sender, instance, **kwargs):
    instance.users.save()
