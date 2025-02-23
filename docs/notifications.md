# 🔔 Real-time Notifications System

## Overview

The notification system provides real-time updates to users through WebSocket connections while persisting notifications in the database.

## Notification Types

1. **Profile Update** (`profile_update`)

   - Triggered when user profile is updated
   - Contains changed fields information

2. **Mention** (`mention`)

   - When a user is mentioned in content
   - Links to the relevant content

3. **System** (`system`)

   - System-level announcements
   - Administrative notifications

4. **Session Management**
   - `session_terminated`: Single session ended
   - `sessions_terminated`: Multiple sessions ended

## WebSocket Integration

### Connection Setup

```javascript
const socket = new WebSocket("ws://your-domain/ws/notifications/");

socket.onmessage = (event) => {
  const notification = JSON.parse(event.data);
  handleNotification(notification);
};

socket.onopen = () => {
  console.log("Connected to notifications");
};

socket.onerror = (error) => {
  console.error("WebSocket error:", error);
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

## REST API Endpoints

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

## Frontend Implementation Guide

### 1. Setup Notification Handler

```javascript
class NotificationHandler {
  constructor() {
    this.socket = null;
    this.connected = false;
    this.handlers = new Map();
  }

  connect() {
    this.socket = new WebSocket("ws://your-domain/ws/notifications/");
    this.setupListeners();
  }

  setupListeners() {
    this.socket.onmessage = (event) => {
      const notification = JSON.parse(event.data);
      this.handleNotification(notification);
    };
  }

  handleNotification(notification) {
    const handler = this.handlers.get(notification.type);
    if (handler) {
      handler(notification);
    }
  }

  registerHandler(type, handler) {
    this.handlers.set(type, handler);
  }
}
```

### 2. Register Notification Handlers

```javascript
const notificationHandler = new NotificationHandler();

// Register handlers for different notification types
notificationHandler.registerHandler("profile_update", (notification) => {
  // Update UI for profile changes
  updateProfileUI(notification.profile_update);
});

notificationHandler.registerHandler("session_terminated", (notification) => {
  // Handle session termination
  showSessionTerminatedAlert();
});
```

### 3. Notification UI Components

```jsx
function NotificationBell({ count }) {
  return (
    <div className="notification-bell">
      <BellIcon />
      {count > 0 && <span className="badge">{count}</span>}
    </div>
  );
}

function NotificationList({ notifications, onMarkRead }) {
  return (
    <div className="notification-list">
      {notifications.map((notification) => (
        <NotificationItem
          key={notification.id}
          notification={notification}
          onMarkRead={onMarkRead}
        />
      ))}
    </div>
  );
}
```

## Error Handling

1. **Connection Loss**

   ```javascript
   socket.onclose = () => {
     setTimeout(() => {
       notificationHandler.connect();
     }, 5000); // Retry after 5 seconds
   };
   ```

2. **Message Processing Errors**
   ```javascript
   try {
     const notification = JSON.parse(event.data);
     handleNotification(notification);
   } catch (error) {
     console.error("Error processing notification:", error);
   }
   ```

## Best Practices

1. **Connection Management**

   - Implement reconnection logic
   - Handle authentication expiration
   - Clean up on component unmount

2. **UI/UX**

   - Show notification badges
   - Implement read/unread status
   - Provide clear notification messages
   - Allow bulk actions (mark all as read)

3. **Performance**
   - Implement pagination for notification list
   - Cache notifications locally
   - Debounce real-time updates
