from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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

class Profile(models.Model):
    users = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='profile')
    badge = models.CharField(max_length=100, default="", blank=True)
    name = models.CharField(max_length=100, default="", blank=True)
    title = models.CharField(max_length=100, default="", blank=True)
    description = models.TextField(default="", blank=True)
    github = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.users.user.username}'s profile"

@receiver(post_save, sender=User)
def create_users(sender, instance, created, **kwargs):
    if created:
        users = Users.objects.create(user=instance)
        Profile.objects.create(users=users)

@receiver(post_save, sender=User)
def save_users(sender, instance, **kwargs):
    instance.users.save()
