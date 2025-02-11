from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.services import NotificationService
from notifications.constants import NotificationTypes
from .models import Profile


@receiver(post_save, sender=Profile)
def notify_profile_update(sender, instance, created, **kwargs):
    """
    Signal handler to create notifications when a profile is updated.
    Tracks specific field changes and notifies via WebSocket.
    """
    if not created:  # Only for updates, not creation
        # Get the changed fields
        update_fields = kwargs.get('update_fields', [])
        
        # If update_fields is empty, consider all fields potentially changed
        if not update_fields:
            update_fields = [
                'badge', 'name', 'title', 'description', 
                'github', 'linkedin', 'twitter'
            ]
        
        NotificationService.create_notification(
            recipient=instance.users.user,
            notification_type=NotificationTypes.PROFILE_UPDATE,
            message=f'Your profile has been updated: {", ".join(update_fields)}',
            content_object=instance,
            extra_data={
                'updated_fields': list(update_fields),
                'profile_id': instance.id,
                'username': instance.users.user.username
            }
        )
