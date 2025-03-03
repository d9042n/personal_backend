from typing import Optional, Any, Dict, Union

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db.models import Model
import logging

from .constants import NotificationTypes
from .models import Notification

logger = logging.getLogger(__name__)
User = get_user_model()


class NotificationService:
    @staticmethod
    def create_notification(
        recipient: User,
        notification_type: str,
        message: str,
        actor: Optional[User] = None,
        content_object: Optional[Model] = None,
        extra_data: Optional[Dict[str, Any]] = None
    ) -> Notification:
        """
        Create a notification and send it through WebSocket.
        
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
            ValidationError: If notification_type is invalid or required fields are missing
            RuntimeError: If WebSocket channel layer is not configured
        """
        if not recipient:
            raise ValidationError("Recipient is required")
            
        if not message:
            raise ValidationError("Message is required")

        # Validate notification type
        if not NotificationTypes.is_valid_type(notification_type):
            raise ValidationError(f"Invalid notification type: {notification_type}")

        try:
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
                "data": notification.data
            }

            # Add profile update specific data if applicable
            if notification_type == NotificationTypes.PROFILE_UPDATE and extra_data:
                payload["profile_update"] = {
                    "fields": extra_data.get('updated_fields', []),
                    "profile_id": extra_data.get('profile_id'),
                    "username": extra_data.get('username')
                }

            # Send WebSocket notification
            channel_layer = get_channel_layer()
            if not channel_layer:
                raise RuntimeError("Channel layer is not configured")

            async_to_sync(channel_layer.group_send)(
                f"user_notifications_{recipient.id}",
                {
                    "type": "notification_message",
                    "data": payload
                }
            )

            return notification

        except Exception as e:
            logger.error(f"Error creating/sending notification: {e}", exc_info=True)
            raise
