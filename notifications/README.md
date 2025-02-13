# 🔔 Notifications Service

A comprehensive real-time notification system providing WebSocket-based notifications for user events, profile updates, and system messages.

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Reference](#-api-reference)
- [WebSocket Integration](#-websocket-integration)
- [Models](#-models)
- [Testing](#-testing)
- [Contributing](#-contributing)

## ✨ Features

- 🚀 Real-time notifications via WebSocket
- 📝 Multiple notification types (Profile Update, Mention, System)
- 🗑️ Soft deletion support
- ✅ Read/Unread status tracking
- 🔗 Generic relations to any model
- 🔌 REST API endpoints with Swagger documentation
- 🔐 Configurable authentication
- ⚡ Asynchronous WebSocket handling
- 📦 Redis channel layer integration
- 🔍 Advanced filtering and search
- 📊 Database indexing for performance

## 🏗 Architecture

### Core Components

1. **Models**

   - `Notification`: Core model with generic relations
   - Supports soft deletion and read status
   - Optimized database indexes

2. **WebSocket Consumer**

   - Asynchronous message handling
   - User-specific notification channels
   - Real-time message delivery

3. **Services**

   - `NotificationService`: Central notification creation
   - Handles WebSocket dispatch
   - Manages notification validation

4. **API Views**
   - RESTful endpoints
   - Swagger documentation
   - Configurable authentication

## 🛠 Installation

1. **Add to INSTALLED_APPS**

```python
INSTALLED_APPS = [
    ...
    'notifications',
]
```

2. **Configure Channel Layer**

```python
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [(os.getenv('REDIS_HOST', 'redis'), 6379)],
        },
    },
}
```

3. **Add WebSocket URLs**

```python
# routing.py
websocket_urlpatterns = [
    re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
]
```

## ⚙️ Configuration

### Environment Variables

| Variable           | Description               | Default |
| ------------------ | ------------------------- | ------- |
| `API_REQUIRE_AUTH` | Enable API authentication | `True`  |
| `REDIS_HOST`       | Redis server host         | `redis` |
| `REDIS_PORT`       | Redis server port         | `6379`  |

### Django Settings

```python
# Authentication configuration
API_REQUIRE_AUTH = True

# WebSocket settings
WSGI_APPLICATION = 'myproject.wsgi.application'
ASGI_APPLICATION = 'myproject.asgi.application'
```

## 🔌 API Reference

### List Notifications

```http
GET /api/notifications/

Response 200:
{
    "id": 1,
    "recipient": {
        "id": 1,
        "username": "testuser"
    },
    "actor": {
        "id": 2,
        "username": "admin"
    },
    "notification_type": "profile_update",
    "message": "Your profile has been updated",
    "data": {
        "updated_fields": ["title"]
    },
    "is_read": false,
    "created_at": "2024-02-15T10:30:00Z"
}
```

### Mark as Read

```http
POST /api/notifications/{id}/mark-read/

Response 200:
{
    "status": "marked as read"
}
```

### Mark All as Read

```http
POST /api/notifications/mark-all-read/

Response 200:
{
    "status": "all marked as read"
}
```

### Delete Notification

```http
DELETE /api/notifications/{id}/delete/

Response 200:
{
    "status": "deleted"
}
```

## 🔌 WebSocket Integration

### Connection Setup

```javascript
const socket = new WebSocket("ws://your-domain/ws/notifications/");

socket.onmessage = function (event) {
  const notification = JSON.parse(event.data);
  console.log("New notification:", notification);
};
```

### Message Format

```javascript
{
    "type": "profile_update",
    "message": "Your profile has been updated",
    "id": 123,
    "created_at": "2024-02-15T10:30:00Z",
    "profile_update": {
        "fields": ["title", "description"],
        "profile_id": 456,
        "username": "john_doe"
    },
    "data": {
        "updated_fields": ["title", "description"]
    }
}
```

## 📦 Models

### Notification Model

| Field               | Type                 | Description                                 |
| ------------------- | -------------------- | ------------------------------------------- |
| `recipient`         | ForeignKey           | User receiving the notification             |
| `actor`             | ForeignKey           | User triggering the notification (optional) |
| `content_type`      | ForeignKey           | ContentType for generic relation            |
| `object_id`         | PositiveIntegerField | ID of related object                        |
| `notification_type` | CharField            | Type of notification                        |
| `message`           | TextField            | Notification message                        |
| `data`              | JSONField            | Additional data                             |
| `is_read`           | BooleanField         | Read status                                 |
| `is_deleted`        | BooleanField         | Soft deletion status                        |
| `created_at`        | DateTimeField        | Creation timestamp                          |
| `updated_at`        | DateTimeField        | Last update timestamp                       |

### Database Indexes

```python
class Meta:
    indexes = [
        models.Index(fields=['recipient', '-created_at']),
        models.Index(fields=['content_type', 'object_id']),
        models.Index(fields=['notification_type']),
        models.Index(fields=['is_read']),
    ]
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python manage.py test notifications

# Run specific test case
python manage.py test notifications.tests.NotificationAPITest
```

### Test Coverage

```bash
coverage run manage.py test notifications
coverage report
```

## 🔧 Development

### Creating New Notifications

```python
from notifications.services import NotificationService
from notifications.constants import NotificationTypes

NotificationService.create_notification(
    recipient=user,
    notification_type=NotificationTypes.PROFILE_UPDATE,
    message="Your profile has been updated",
    actor=request.user,
    content_object=profile,
    extra_data={'updated_fields': ['title']}
)
```

### Signal Integration

```python
@receiver(post_save, sender=Profile)
def notify_profile_update(sender, instance, created, **kwargs):
    if not created:
        NotificationService.create_notification(
            recipient=instance.user,
            notification_type=NotificationTypes.PROFILE_UPDATE,
            message='Your profile has been updated',
            content_object=instance
        )
```

## 🔒 Security Considerations

1. **Authentication**

   - Configurable API authentication
   - WebSocket connection validation
   - User-specific channels

2. **Data Protection**

   - Soft deletion support
   - User data isolation
   - Input validation

3. **Performance**
   - Optimized database queries
   - Indexed fields
   - Asynchronous WebSocket handling

## 📚 Additional Resources

- [Django Channels Documentation](https://channels.readthedocs.io/)
- [WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [Django Generic Relations](https://docs.djangoproject.com/en/stable/ref/contrib/contenttypes/)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Write tests for new features
4. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Made with ❤️ by the Personal Website Team
