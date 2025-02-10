from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Profile
from .constants import NotificationTypes
from .services import NotificationService


@receiver(post_save, sender=Profile)
def notify_profile_update(sender, instance, created, **kwargs):
    """
    Signal handler to create notifications when a profile is updated
    """
    if not created:  # Only for updates, not creation
        NotificationService.create_notification(
            recipient=instance.users.user,
            notification_type=NotificationTypes.PROFILE_UPDATE,
            message='Your profile has been updated',
            content_object=instance,
            extra_data={
                'updated_fields': kwargs.get('update_fields', [])
            }
        )
