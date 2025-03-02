# Notifications API Documentation

## Overview

The Notifications API provides endpoints for managing real-time notifications. It supports both REST API endpoints and WebSocket connections for real-time updates.

## WebSocket Connection

### Connect to Notifications WebSocket

- **URL**: `ws://domain/ws/notifications/`
- **Authentication**: Required (via token query parameter)
- **Connection URL**: `ws://domain/ws/notifications/?token=<your_jwt_token>`

### WebSocket Events

#### Receive Notification

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

```json
{
  "type": "notification.read",
  "data": {
    "id": "string",
    "is_read": true
  }
}
```

## REST API Endpoints

### List Notifications

- **URL**: `/api/notifications/`
- **Method**: `GET`
- **Authentication**: Required
- **Query Parameters**:
  - `cursor`: Pagination cursor
  - `page_size`: Items per page (default: 20)
  - `is_read`: Filter by read status (optional)
- **Response**:
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

- **URL**: `/api/notifications/{id}/`
- **Method**: `GET`
- **Authentication**: Required
- **Response**:
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

- **URL**: `/api/notifications/{id}/read/`
- **Method**: `PATCH`
- **Authentication**: Required
- **Response**: `200 OK`

### Mark All Notifications as Read

- **URL**: `/api/notifications/read_all/`
- **Method**: `PATCH`
- **Authentication**: Required
- **Response**: `200 OK`

### Delete Notification

- **URL**: `/api/notifications/{id}/`
- **Method**: `DELETE`
- **Authentication**: Required
- **Response**: `204 No Content`

## Notification Types

The system supports various notification types:

1. `USER_MENTION` - When a user is mentioned
2. `SYSTEM_UPDATE` - System-level notifications
3. `DIRECT_MESSAGE` - Direct message notifications

Each type may include additional data in the `data` field of the notification object.

## Error Responses

All endpoints may return the following error responses:

- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Notification not found
- `500 Internal Server Error`: Server-side error

## WebSocket Error Handling

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
