from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
import logging

from .constants import NotificationTypes
from .models import Notification

logger = logging.getLogger(__name__)


class NotificationService:
    @staticmethod
    def create_notification(recipient, notification_type, message, actor=None, content_object=None, extra_data=None):
        """
        Create a notification and send it through WebSocket
        
        Args:
            recipient: User who will receive the notification
            notification_type: Type of notification (must be valid)
            message: Notification message
            actor: User who triggered the notification (optional)
            content_object: Related object (optional)
            extra_data: Additional JSON data (optional)
            
        Returns:
            Created notification instance
            
        Raises:
            ValidationError: If notification_type is invalid
        """
        # Validate notification type
        if not NotificationTypes.is_valid_type(notification_type):
            raise ValidationError(f"Invalid notification type: {notification_type}")

        # Create notification
        notification = Notification.objects.create(
            recipient=recipient,
            actor=actor,
            notification_type=notification_type,
            message=message,
            content_type=ContentType.objects.get_for_model(content_object) if content_object else None,
            object_id=content_object.id if content_object else None,
            data=extra_data or {}
        )

        # Prepare WebSocket payload
        payload = {
            "id": notification.id,
            "type": notification_type,
            "message": message,
            "created_at": notification.created_at.isoformat(),
            "data": notification.data,
            "profile_update": {
                "fields": extra_data.get('updated_fields', []) if extra_data else [],
                "profile_id": extra_data.get('profile_id') if extra_data else None,
                "username": extra_data.get('username') if extra_data else None
            } if notification_type == NotificationTypes.PROFILE_UPDATE else None
        }

        # Send WebSocket notification
        try:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_notifications_{recipient.id}",
                {
                    "type": "notification_message",
                    "data": payload
                }
            )
        except Exception as e:
            logger.error(f"Error sending WebSocket notification: {e}", exc_info=True)

        return notification
