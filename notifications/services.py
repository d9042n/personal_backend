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
            message: Message content
            actor: User who triggered the notification (optional)
            content_object: Related object (optional)
            extra_data: Additional JSON data (optional)
            
        Returns:
            Created notification instance
            
        Raises:
            ValidationError: If notification_type is invalid or required fields are missing
            RuntimeError: If WebSocket channel layer is not configured
        """
        logger.info(f"Creating {notification_type} notification for recipient: {recipient.username}")
        
        if not recipient:
            logger.error("Recipient is required for notification creation")
            raise ValidationError("Recipient is required")
            
        if not message:
            logger.error("Message is required for notification creation")
            raise ValidationError("Message is required")

        # Validate notification type
        if not NotificationTypes.is_valid_type(notification_type):
            logger.error(f"Invalid notification type attempted: {notification_type}")
            raise ValidationError(f"Invalid notification type: {notification_type}")

        try:
            logger.debug(f"Creating notification with message: {message}")
            
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
            
            logger.debug(f"Notification created with ID: {notification.id}")

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
                logger.debug("Adding profile update specific data to notification")
                payload["profile_update"] = {
                    "fields": extra_data.get('updated_fields', []),
                    "profile_id": extra_data.get('profile_id'),
                    "username": extra_data.get('username')
                }

            # Send WebSocket notification
            channel_layer = get_channel_layer()
            if not channel_layer:
                logger.error("Channel layer is not configured for WebSocket notifications")
                raise RuntimeError("Channel layer is not configured")

            logger.debug(f"Sending WebSocket notification to user_{recipient.id}")
            async_to_sync(channel_layer.group_send)(
                f"user_notifications_{recipient.id}",
                {
                    "type": "notification_message",
                    "data": payload
                }
            )
            
            logger.info(f"Notification {notification.id} created and sent successfully")
            return notification

        except Exception as e:
            logger.error(f"Error creating/sending notification: {str(e)}", exc_info=True)
            raise

    @staticmethod
    def mark_notifications_as_read(recipient: User, notification_ids: Optional[list] = None) -> int:
        """
        Mark notifications as read for a user.
        
        Args:
            recipient: The user whose notifications to mark as read
            notification_ids: Optional list of specific notification IDs to mark as read
            
        Returns:
            Number of notifications marked as read
        """
        try:
            logger.info(f"Marking notifications as read for user: {recipient.username}")
            
            # Build query for unread notifications
            query = Notification.objects.filter(
                recipient=recipient,
                is_read=False,
                is_deleted=False
            )
            
            # Filter by specific IDs if provided
            if notification_ids:
                logger.debug(f"Marking specific notifications as read: {notification_ids}")
                query = query.filter(id__in=notification_ids)
            
            # Update notifications
            count = query.update(is_read=True)
            
            logger.info(f"Marked {count} notifications as read for user: {recipient.username}")
            return count
            
        except Exception as e:
            logger.error(f"Error marking notifications as read for user {recipient.username}: {str(e)}", exc_info=True)
            raise

    @staticmethod
    def get_unread_count(recipient: User) -> int:
        """
        Get count of unread notifications for a user.
        
        Args:
            recipient: The user whose unread notifications to count
            
        Returns:
            Count of unread notifications
        """
        try:
            count = Notification.objects.filter(
                recipient=recipient,
                is_read=False,
                is_deleted=False
            ).count()
            
            logger.debug(f"User {recipient.username} has {count} unread notifications")
            return count
            
        except Exception as e:
            logger.error(f"Error getting unread count for user {recipient.username}: {str(e)}", exc_info=True)
            raise
