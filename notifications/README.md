# 🔔 Notifications Service

A comprehensive real-time notification system built with Django and WebSocket support, providing seamless integration for user events and system notifications.

## ✨ Core Features

### 🚀 Real-time Notifications

- WebSocket-based instant notifications
- Automatic connection management
- Session-aware delivery
- Channel-based user grouping

### 📝 Notification Types

- `PROFILE_UPDATE`: User profile changes
- `MENTION`: User mentions in content
- `SYSTEM`: System-level notifications
- `SESSION_TERMINATED`: Single session termination
- `SESSIONS_TERMINATED`: Multiple sessions termination

### 🔌 API Integration

- RESTful endpoints for notification management
- Swagger/OpenAPI documentation
- Rate limiting support
- Authentication-aware endpoints

### 💾 Data Management

- Soft deletion support
- Read/Unread status tracking
- Generic relations to any model
- Timestamp tracking (created/updated)
- JSON field for flexible data storage

## 📋 API Endpoints

### List Notifications

```http
GET /api/notifications/

Response 200:
{
    "count": 1,
    "results": [
        {
            "id": 1,
            "recipient": {
                "id": 1,
                "username": "johndoe"
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
            "created_at": "2025-02-10T15:30:00Z"
        }
    ]
}
```

### Mark as Read

```http
PATCH /api/notifications/{id}/read/

Response 200:
{
    "id": 1,
    "is_read": true,
    ...
}
```

### Mark All as Read

```http
PATCH /api/notifications/read_all/

Response 200:
[
    {
        "id": 1,
        "is_read": true,
        ...
    }
]
```

### Delete Notification

```http
DELETE /api/notifications/{id}/

Response 204 No Content
```

## 🔌 WebSocket Integration

### Connection Setup

```javascript
const socket = new WebSocket("ws://your-domain/ws/notifications/");

socket.onmessage = (event) => {
  const notification = JSON.parse(event.data);
  handleNotification(notification);
};
```

### Message Format

```typescript
interface NotificationMessage {
  type: string; // Notification type
  message: string; // Display message
  id: number; // Notification ID
  created_at: string; // ISO timestamp
  data: {
    // Additional data
    [key: string]: any;
  };
  profile_update?: {
    // For profile updates
    fields: string[];
    profile_id: number;
    username: string;
  };
}
```

## 🛠️ Service Usage

### Creating Notifications

```python
from notifications.services import NotificationService
from notifications.constants import NotificationTypes

NotificationService.create_notification(
    recipient=user,
    notification_type=NotificationTypes.PROFILE_UPDATE,
    message="Your profile has been updated",
    actor=request.user,  # optional
    content_object=profile,  # optional
    extra_data={
        'updated_fields': ['title'],
        'profile_id': profile.id,
        'username': user.username
    }
)
```

### Signal Integration

```python
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Profile)
def notify_profile_update(sender, instance, created, **kwargs):
    if not created:
        NotificationService.create_notification(...)
```

## 📊 Data Models

### Notification Model

| Field             | Type          | Description                  |
| ----------------- | ------------- | ---------------------------- |
| recipient         | ForeignKey    | User receiving notification  |
| actor             | ForeignKey    | User triggering notification |
| content_type      | ForeignKey    | Related object type          |
| object_id         | PositiveInt   | Related object ID            |
| notification_type | CharField     | Type of notification         |
| message           | TextField     | Notification message         |
| data              | JSONField     | Additional data              |
| is_read           | BooleanField  | Read status                  |
| is_deleted        | BooleanField  | Soft deletion status         |
| created_at        | DateTimeField | Creation timestamp           |
| updated_at        | DateTimeField | Last update timestamp        |

## 🔒 Security Features

- Authentication-aware WebSocket connections
- Permission-based access control
- User-specific notification isolation
- Soft deletion for data protection
- Validation for notification types

## ⚙️ Configuration

Environment variables:

```env
API_REQUIRE_AUTH=True    # Require authentication for API
REDIS_HOST=redis        # Redis host for WebSocket
```

## 🧪 Testing

```bash
# Run all notification tests
python manage.py test notifications

# Run specific test class
python manage.py test notifications.tests.NotificationAPITest
```

## 📦 Dependencies

- Django 4.2+
- Django REST Framework
- Django Channels
- Redis (for WebSocket)
- drf-yasg (for API documentation)

## 🔄 Performance Considerations

- Indexed fields for quick lookups
- Soft deletion instead of hard deletes
- Efficient WebSocket message delivery
- Optimized database queries
- Async WebSocket consumers

## 🎯 Use Cases

1. **Profile Updates**

   - Real-time notification when user profile is updated
   - Detailed tracking of changed fields

2. **Session Management**

   - Notifications for session termination
   - Multi-session termination alerts

3. **System Notifications**

   - Administrative announcements
   - System maintenance alerts

4. **User Interactions**
   - Mention notifications
   - User activity updates

---

Made with ❤️ for the Personal Website Project
