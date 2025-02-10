# Django Notifications App

A flexible and real-time notification system for Django applications with WebSocket support.

## Features

- Real-time notifications using WebSocket
- Multiple notification types support
- Soft deletion of notifications
- Read/Unread status tracking
- Generic relations to any model
- REST API endpoints
- Authentication-optional endpoints
- Swagger/OpenAPI documentation
- WebSocket real-time updates
- Redis channel layer support

## Installation

1. Add 'notifications' to your INSTALLED_APPS:

```python
INSTALLED_APPS = [
    ...
    'notifications',
    'channels',  # Required for WebSocket support
]
```

2. Add the WebSocket routing to your project's routing.py:

```python
from django.urls import re_path
from notifications.consumers import NotificationConsumer

websocket_urlpatterns = [
    re_path(r'ws/notifications/$', NotificationConsumer.as_asgi()),
]
```

3. Configure Redis for channel layers in settings.py:

```python
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(os.getenv('REDIS_HOST', 'redis'), 6379)],
        },
    },
}
```

4. Add the notification URLs to your project's urls.py:

```python
from django.urls import path, include

urlpatterns = [
    ...
    path('api/notifications/', include('notifications.urls')),
]
```

## Configuration

### Environment Variables

- `API_REQUIRE_AUTH`: Control whether API endpoints require authentication (default: True)
- `REDIS_HOST`: Redis host for WebSocket channel layer (default: 'redis')

### Available Settings

```python
# settings.py

# API Authentication settings
API_REQUIRE_AUTH = os.getenv('API_REQUIRE_AUTH', 'True').lower() == 'true'
```

## API Endpoints

### 1. List Notifications

```
GET /api/notifications/

Response:
{
    "id": 1,
    "recipient": {"id": 1, "username": "testuser"},
    "actor": {"id": 2, "username": "admin"},
    "notification_type": "profile_update",
    "message": "Your profile has been updated",
    "data": {"updated_fields": ["title"]},
    "is_read": false,
    "created_at": "2025-02-10T15:30:00Z"
}
```

### 2. Mark Notification as Read

```
POST /api/notifications/{id}/mark-read/

Response:
{
    "status": "marked as read"
}
```

### 3. Mark All Notifications as Read

```
POST /api/notifications/mark-all-read/

Response:
{
    "status": "all marked as read"
}
```

### 4. Delete Notification

```
DELETE /api/notifications/{id}/delete/

Response:
{
    "status": "deleted"
}
```

## WebSocket Integration

### Connecting to WebSocket

```javascript
// Connect to notification WebSocket
const socket = new WebSocket("ws://your-domain/ws/notifications/");

// Listen for messages
socket.onmessage = function (event) {
  const notification = JSON.parse(event.data);
  console.log("New notification:", notification);
};
```

### Marking Notifications as Read via WebSocket

```javascript
socket.send(
  JSON.stringify({
    type: "mark_read",
    notification_id: 1,
  })
);
```

## Creating Notifications

Use the NotificationService to create new notifications:

```python
from notifications.services import NotificationService
from notifications.constants import NotificationTypes

# Create a notification
NotificationService.create_notification(
    recipient=user,
    notification_type=NotificationTypes.PROFILE_UPDATE,
    message="Your profile has been updated",
    actor=request.user,  # optional
    content_object=profile,  # optional
    extra_data={'updated_fields': ['title']}  # optional
)
```

## Notification Types

Available notification types (customizable in `constants.py`):

- `profile_update`: Profile update notifications
- `mention`: User mention notifications
- `system`: System notifications

## Models

### Notification Model Fields

- `recipient`: User who receives the notification
- `actor`: User who triggered the notification (optional)
- `notification_type`: Type of notification
- `message`: Notification message
- `data`: Additional JSON data
- `is_read`: Read status
- `is_deleted`: Soft deletion status
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

## Testing

Run the tests:

```bash
python manage.py test notifications
```

## Example Usage

### Signal Integration

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.services import NotificationService

@receiver(post_save, sender=YourModel)
def notify_update(sender, instance, created, **kwargs):
    if not created:
        NotificationService.create_notification(
            recipient=instance.user,
            notification_type='model_update',
            message=f'Your {instance._meta.verbose_name} has been updated'
        )
```

### Frontend Integration Example

```javascript
// Connect to WebSocket
const connectWebSocket = () => {
  const socket = new WebSocket("ws://your-domain/ws/notifications/");

  socket.onmessage = (event) => {
    const notification = JSON.parse(event.data);
    showNotification(notification);
  };

  socket.onclose = () => {
    // Reconnect on close
    setTimeout(connectWebSocket, 1000);
  };

  return socket;
};

// Show notification
const showNotification = (notification) => {
  // Implement your notification UI logic here
};

// Initialize WebSocket connection
const socket = connectWebSocket();
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.
