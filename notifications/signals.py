from typing import Optional, Set, Type, Any

from django.db.models.signals import post_save
from django.dispatch import receiver
import logging

from users.models import Profile
from .constants import NotificationTypes
from .services import NotificationService

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Profile)
def notify_profile_update(
    sender: Type[Profile],
    instance: Profile,
    created: bool,
    **kwargs: Any
) -> None:
    """
    Signal handler to create notifications when a profile is updated.
    
    This handler listens for profile updates and creates a notification
    for the user when their profile is modified. It only triggers for
    updates, not for new profile creation.
    
    Args:
        sender: The model class (Profile)
        instance: The actual profile instance that was saved
        created: Boolean indicating if this is a new instance
        **kwargs: Additional signal arguments including update_fields
    """
    if created:  # Skip for new profiles
        return

    try:
        # Get the updated fields from kwargs or use an empty set
        updated_fields: Optional[Set[str]] = kwargs.get('update_fields')
        
        NotificationService.create_notification(
            recipient=instance.users.user,  # Access user through Users model
            notification_type=NotificationTypes.PROFILE_UPDATE,
            message='Your profile has been updated',
            content_object=instance,
            extra_data={
                'updated_fields': list(updated_fields) if updated_fields else [],
                'profile_id': instance.id,
                'username': instance.users.user.username
            }
        )
    except Exception as e:
        logger.error(
            f"Failed to create profile update notification for user {instance.users.user.id}: {e}",
            exc_info=True
        )
