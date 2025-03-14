# 🔔 Notifications API Documentation

[![API Status](https://img.shields.io/badge/API-Active-success)](https://github.com/yourusername/personal_backend)
[![WebSockets](https://img.shields.io/badge/WebSockets-Enabled-brightgreen)](https://channels.readthedocs.io/)
[![Django Channels](https://img.shields.io/badge/Django_Channels-4.2-purple)](https://channels.readthedocs.io/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 📑 Table of Contents

1. [Overview](#overview)
2. [WebSocket Connection](#websocket-connection)
3. [REST API Endpoints](#rest-api-endpoints)
4. [Notification Types](#notification-types)
5. [Error Handling](#error-handling)
6. [Best Practices](#best-practices)

## 🎯 Overview

The Notifications API provides a comprehensive real-time notification system using both REST API endpoints and WebSocket connections. This dual approach ensures that users receive instant updates while maintaining the ability to query notification history and manage notification settings.

## 🔌 WebSocket Connection

### Connect to Notifications WebSocket

Establish a real-time connection to receive notifications as they occur.

- **URL**: `ws://domain/ws/notifications/`
- **Authentication**: Required (via token query parameter)
- **Connection URL**: `ws://domain/ws/notifications/?token=<your_jwt_token>`

### WebSocket Events

#### Receive Notification

When a new notification is created, the client receives this event:

```json
{
  "type": "notification.received",
  "data": {
    "id": "string",
    "type": "string",
    "message": "string",
    "created_at": "datetime",
    "is_read": false,
    "data": {}
  }
}
```

#### Mark as Read Acknowledgment

After marking a notification as read, the client receives this confirmation:

```json
{
  "type": "notification.read",
  "data": {
    "id": "string",
    "is_read": true
  }
}
```

#### Client Actions

Clients can send the following actions to the WebSocket:

```json
{
  "action": "mark_read",
  "notification_id": "string"
}
```

## 📡 REST API Endpoints

### List Notifications

Retrieve a paginated list of notifications for the authenticated user.

- **URL**: `/api/notifications/`
- **Method**: `GET`
- **Authentication**: Required
- **Query Parameters**:
  - `cursor`: Pagination cursor
  - `page_size`: Items per page (default: 20)
  - `is_read`: Filter by read status (optional)
- **Response** (200 OK):
  ```json
  {
    "data": {
      "results": [
        {
          "id": "string",
          "type": "string",
          "message": "string",
          "created_at": "datetime",
          "is_read": boolean,
          "data": {}
        }
      ],
      "next_cursor": "string",
      "previous_cursor": "string"
    }
  }
  ```

### Get Single Notification

Retrieve details for a specific notification.

- **URL**: `/api/notifications/{id}/`
- **Method**: `GET`
- **Authentication**: Required
- **Response** (200 OK):
  ```json
  {
    "data": {
      "id": "string",
      "type": "string",
      "message": "string",
      "created_at": "datetime",
      "is_read": boolean,
      "data": {}
    }
  }
  ```

### Mark Notification as Read

Mark a specific notification as read.

- **URL**: `/api/notifications/{id}/read/`
- **Method**: `PATCH`
- **Authentication**: Required
- **Response** (200 OK):
  ```json
  {
    "data": {
      "id": "string",
      "is_read": true
    }
  }
  ```

### Mark All Notifications as Read

Mark all notifications for the authenticated user as read.

- **URL**: `/api/notifications/read_all/`
- **Method**: `PATCH`
- **Authentication**: Required
- **Response** (200 OK):
  ```json
  {
    "data": {
      "count": 5,
      "message": "5 notifications marked as read"
    }
  }
  ```

### Delete Notification

Delete a specific notification.

- **URL**: `/api/notifications/{id}/`
- **Method**: `DELETE`
- **Authentication**: Required
- **Response**: `204 No Content`

## 📋 Notification Types

The system supports various notification types, each with specific data structures:

### 1. PROFILE_UPDATE

Triggered when a user's profile is updated.

```json
{
  "type": "profile_update",
  "data": {
    "updated_fields": ["name", "title", "description"],
    "profile_id": "string",
    "username": "string"
  }
}
```

### 2. MENTION

Triggered when a user is mentioned in content.

```json
{
  "type": "mention",
  "data": {
    "mentioned_by": "username",
    "content_id": "string",
    "content_type": "string"
  }
}
```

### 3. SYSTEM

System-level notifications for important updates.

```json
{
  "type": "system",
  "data": {
    "update_type": "string",
    "importance": "high|medium|low"
  }
}
```

### 4. SESSION_TERMINATED

Triggered when a user's session is terminated.

```json
{
  "type": "session_terminated",
  "data": {
    "session_id": "string",
    "device_info": "string",
    "terminated_at": "datetime"
  }
}
```

### 5. SESSIONS_TERMINATED

Triggered when multiple sessions for a user are terminated.

```json
{
  "type": "sessions_terminated",
  "data": {
    "session_count": "number",
    "terminated_at": "datetime"
  }
}
```

## ⚠️ Error Handling

### REST API Errors

All endpoints may return the following error responses:

| Status Code | Description  | Common Causes                  |
| ----------- | ------------ | ------------------------------ |
| 400         | Bad Request  | Invalid input data             |
| 401         | Unauthorized | Missing/invalid authentication |
| 403         | Forbidden    | Insufficient permissions       |
| 404         | Not Found    | Notification not found         |
| 500         | Server Error | Internal processing error      |

### WebSocket Error Handling

WebSocket connections may receive error messages in the following format:

```json
{
  "type": "error",
  "data": {
    "code": "string",
    "message": "string"
  }
}
```

Common error codes:

- `authentication_failed`: Invalid or missing authentication token
- `connection_error`: General connection error
- `rate_limit_exceeded`: Too many connection attempts

## 💡 Best Practices

### Client Implementation

1. **Maintain WebSocket Connection**

   - Implement reconnection logic with exponential backoff
   - Handle connection errors gracefully

2. **Notification Storage**

   - Cache notifications locally for offline access
   - Sync with server when connection is restored

3. **User Experience**
   - Show real-time notifications without disrupting user flow
   - Provide clear notification grouping and prioritization

### Server Considerations

1. **Performance**

   - Notifications are delivered with minimal latency (<500ms)
   - WebSocket connections are maintained efficiently

2. **Reliability**
   - Notifications are guaranteed to be delivered at least once
   - Missed notifications can be retrieved via REST API

---

For more information about the API, refer to the [main documentation](../README.md).
