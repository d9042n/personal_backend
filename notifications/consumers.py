import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from django.contrib.auth.models import AnonymousUser


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Check if authentication is required and user is anonymous
        if settings.API_REQUIRE_AUTH and isinstance(self.scope["user"], AnonymousUser):
            await self.close()
            return

        # If authentication is not required but user is anonymous, only allow connection
        # but don't set up notifications
        if isinstance(self.scope["user"], AnonymousUser):
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

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            # Leave room group
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        if isinstance(self.scope["user"], AnonymousUser):
            return

        text_data_json = json.loads(text_data)
        message_type = text_data_json.get("type")

        if message_type == "mark_read":
            notification_id = text_data_json.get("notification_id")
            await self.mark_notification_as_read(notification_id)

    async def notification_message(self, event):
        # Don't send notifications to anonymous users
        if isinstance(self.scope["user"], AnonymousUser):
            return

        # Send notification to WebSocket
        await self.send(text_data=json.dumps(event["data"]))

    @database_sync_to_async
    def mark_notification_as_read(self, notification_id):
        from .models import Notification
        try:
            notification = Notification.objects.get(
                id=notification_id,
                recipient_id=self.user_id
            )
            notification.mark_as_read()
        except Notification.DoesNotExist:
            pass
