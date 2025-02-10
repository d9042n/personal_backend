from django.db.models.signals import post_save
from django.dispatch import receiver

from notifications.services import NotificationService
from .models import Profile


@receiver(post_save, sender=Profile)
def notify_profile_update(sender, instance, created, **kwargs):
    if not created:  # Only for updates, not creation
        NotificationService.create_notification(
            recipient=instance.users.user,
            notification_type='profile_update',
            message='Your profile has been updated',
            content_object=instance,
            extra_data={
                'updated_fields': kwargs.get('update_fields', [])
            }
        )
