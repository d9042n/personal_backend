import json
from typing import Optional, Dict, Any, Union

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
import logging

from .models import Notification

logger = logging.getLogger(__name__)
User = get_user_model()


class NotificationConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for handling real-time notifications.
    
    This consumer manages WebSocket connections for real-time notification delivery.
    It handles user authentication, connection management, and notification message
    processing.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id: Optional[int] = None
        self.room_group_name: Optional[str] = None

    async def connect(self) -> None:
        """
        Handle WebSocket connection.
        
        Authenticates the user and sets up the notification channel if authorized.
        Closes the connection for unauthorized users when authentication is required.
        """
        try:
            # Check if authentication is required and user is anonymous
            if settings.API_REQUIRE_AUTH and isinstance(self.scope["user"], AnonymousUser):
                logger.warning("Anonymous user attempted to connect when authentication is required")
                await self.close()
                return

            # If authentication is not required but user is anonymous, only allow connection
            # but don't set up notifications
            if isinstance(self.scope["user"], AnonymousUser):
                logger.info("Anonymous user connected (notifications disabled)")
                await self.accept()
                return

            self.user_id = self.scope["user"].id
            self.room_group_name = f"user_notifications_{self.user_id}"

            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()
            logger.info(f"User {self.scope['user'].username} connected to notifications WebSocket")

        except Exception as e:
            logger.error(f"Error in WebSocket connection: {str(e)}", exc_info=True)
            await self.close()

    async def disconnect(self, close_code: int) -> None:
        """
        Handle WebSocket disconnection.
        
        Removes the user from the notification channel group.
        
        Args:
            close_code: WebSocket close code
        """
        try:
            if hasattr(self, 'room_group_name'):
                # Leave room group
                await self.channel_layer.group_discard(
                    self.room_group_name,
                    self.channel_name
                )
                if not isinstance(self.scope["user"], AnonymousUser):
                    logger.info(f"User {self.scope['user'].username} disconnected from notifications WebSocket")
        except Exception as e:
            logger.error(f"Error in WebSocket disconnection: {str(e)}", exc_info=True)

    async def receive(self, text_data: str) -> None:
        """
        Handle incoming WebSocket messages.
        
        Currently supports marking notifications as read.
        
        Args:
            text_data: JSON string containing message data
        """
        if isinstance(self.scope["user"], AnonymousUser):
            logger.warning("Anonymous user attempted to send WebSocket message")
            return

        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get("type")

            if message_type == "mark_read":
                notification_id = text_data_json.get("notification_id")
                if notification_id:
                    logger.debug(f"Marking notification {notification_id} as read for user {self.scope['user'].username}")
                    await self.mark_notification_as_read(notification_id)
            else:
                logger.warning(f"Unknown message type received: {message_type}")
        except json.JSONDecodeError:
            logger.error("Invalid JSON received in WebSocket message")
        except Exception as e:
            logger.error(f"Error processing WebSocket message: {str(e)}", exc_info=True)

    async def notification_message(self, event: Dict[str, Any]) -> None:
        """
        Handle incoming notification messages.
        
        Sends notifications to connected WebSocket clients.
        
        Args:
            event: Dictionary containing notification data
        """
        if isinstance(self.scope["user"], AnonymousUser):
            return

        try:
            data = event["data"]
            await self.send(text_data=json.dumps(data))
            logger.debug(f"Sent notification to user {self.scope['user'].username}: {data.get('message', '')[:50]}")
        except Exception as e:
            logger.error(f"Error sending notification message: {str(e)}", exc_info=True)

    @database_sync_to_async
    def mark_notification_as_read(self, notification_id: Union[int, str]) -> None:
        """
        Mark a notification as read.
        
        Args:
            notification_id: ID of the notification to mark as read
        """
        try:
            notification = Notification.objects.get(
                id=notification_id,
                recipient_id=self.user_id
            )
            notification.mark_as_read()
            logger.info(f"Notification {notification_id} marked as read by user {self.scope['user'].username}")
        except Notification.DoesNotExist:
            logger.warning(f"Notification {notification_id} not found for user {self.user_id}")
        except Exception as e:
            logger.error(f"Error marking notification as read: {str(e)}", exc_info=True)
