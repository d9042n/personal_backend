"""
WebSocket routing configuration for the notifications app.

This module defines the WebSocket URL patterns for real-time notifications.
It maps WebSocket endpoints to their corresponding consumers.

Available WebSocket endpoints:
    ws/notifications/ - Endpoint for real-time notification updates
"""

from django.urls import re_path
from typing import List

from . import consumers

# WebSocket URL patterns
websocket_urlpatterns: List[re_path] = [
    re_path(
        r'ws/notifications/$',
        consumers.NotificationConsumer.as_asgi(),
        name='notifications_ws'
    ),
]
