# 🔔 Notifications Service

A real-time notification system integrated with the Users service, providing WebSocket-based notifications for profile
updates and system events.

## ✨ Features

- 🚀 Real-time notifications via WebSocket
- 📝 Multiple notification types (Profile Update, Mention, System)
- 🗑️ Soft deletion support
- ✅ Read/Unread status tracking
- 🔗 Generic relations to any model
- 🔌 REST API endpoints
- 🔐 Configurable authentication
- ⚡ WebSocket real-time updates
- 📦 Redis channel layer integration

## 📋 System Architecture

### Integration with Users Service

The notification system is tightly integrated with the Users service to provide automatic notifications for:

- Profile updates
- User mentions
- System notifications

### Environment Configuration

The service behavior can be configured through environment variables:

| Variable           | Description                | Default |
| ------------------ | -------------------------- | ------- |
| `API_REQUIRE_AUTH` | Control API authentication | `True`  |
| `REDIS_HOST`       | Redis host for WebSocket   | `redis` |

## 🔌 API Endpoints

### List Notifications

```http
GET /api/notifications/

Response 200:
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

### Connection

```javascript
const socket = new WebSocket("ws://your-domain/ws/notifications/");

socket.onmessage = function (event) {
  const notification = JSON.parse(event.data);
  console.log("New notification:", notification);
};
```

### Mark as Read via WebSocket

```javascript
socket.send(
  JSON.stringify({
    type: "mark_read",
    notification_id: 1,
  })
);
```

## 📝 Creating Notifications

Use the NotificationService to create new notifications:

```python
from notifications.services import NotificationService
from notifications.constants import NotificationTypes

NotificationService.create_notification(
    recipient=user,
    notification_type=NotificationTypes.PROFILE_UPDATE,
    message="Your profile has been updated",
    actor=request.user,  # optional
    content_object=profile,  # optional
    extra_data={'updated_fields': ['title']}  # optional
)
```

## 📊 Notification Types

Available types in `constants.py`:

- `profile_update`: Profile update notifications
- `mention`: User mention notifications
- `system`: System notifications

## 📚 Data Models

### Notification Model

| Field               | Type          | Description                      |
| ------------------- | ------------- | -------------------------------- |
| `recipient`         | ForeignKey    | User receiving the notification  |
| `actor`             | ForeignKey    | User triggering the notification |
| `notification_type` | CharField     | Type of notification             |
| `message`           | TextField     | Notification message             |
| `data`              | JSONField     | Additional data                  |
| `is_read`           | BooleanField  | Read status                      |
| `is_deleted`        | BooleanField  | Soft deletion status             |
| `created_at`        | DateTimeField | Creation timestamp               |

## 🧪 Testing

Run the test suite:

```bash
python manage.py test notifications
```

## 💡 Example: Profile Update Flow

1. User updates their profile
2. Signal handler triggers:

```python
@receiver(post_save, sender=Profile)
def notify_profile_update(sender, instance, created, **kwargs):
    if not created:
        NotificationService.create_notification(
            recipient=instance.users.user,
            notification_type=NotificationTypes.PROFILE_UPDATE,
            message='Your profile has been updated',
            content_object=instance
        )
```

3. WebSocket delivers real-time notification
4. Frontend receives and displays notification:

```javascript
const connectWebSocket = () => {
  const socket = new WebSocket("ws://your-domain/ws/notifications/");

  socket.onmessage = (event) => {
    const notification = JSON.parse(event.data);
    showNotification(notification);
  };

  return socket;
};
```

# 🔔 Real-time Profile Update Notifications

## WebSocket Integration for Profile Updates

### Connection Setup

```javascript
const socket = new WebSocket("ws://your-domain/ws/notifications/");

socket.onmessage = function (event) {
  const notification = JSON.parse(event.data);

  // Handle profile updates
  if (notification.type === "profile_update") {
    const { fields, profile_id, username } = notification.profile_update;

    // Update UI with changed fields
    updateProfileUI(fields, profile_id, username);
  }
};
```

### Profile Update Notification Format

```json
{
  "type": "profile_update",
  "message": "Your profile has been updated: title, description",
  "id": 123,
  "created_at": "2024-03-15T10:30:00Z",
  "profile_update": {
    "fields": ["title", "description"],
    "profile_id": 456,
    "username": "john_doe"
  },
  "data": {
    "updated_fields": ["title", "description"],
    "profile_id": 456,
    "username": "john_doe"
  }
}
```

### Frontend Integration Example

```javascript
function updateProfileUI(changedFields, profileId, username) {
  // Refresh specific profile sections based on changed fields
  changedFields.forEach((field) => {
    switch (field) {
      case "title":
        refreshProfileTitle(profileId);
        break;
      case "description":
        refreshProfileDescription(profileId);
        break;
      // Handle other fields...
    }
  });

  // Show notification toast
  showNotification(`Profile updated: ${changedFields.join(", ")}`);
}
```

## Features

- 🚀 Real-time profile update notifications
- 📝 Detailed change tracking
- 🔌 WebSocket-based delivery
- 🔐 Authenticated connections
- 📦 Field-specific updates

---

Made with ❤️ for the Personal Website Project
