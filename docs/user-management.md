# 👤 User Management

## Overview

The User Management service provides a comprehensive API for managing user accounts, profiles, and sessions. This section details the available endpoints and their functionalities.

## User Registration

### Registration Endpoint

Users can register by providing their username, email, and password.

```http
POST /api/users/

Request Body:
{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "users": {
        "profile": {
            "name": "John Doe",
            "title": "Software Developer",
            "is_available": true
        }
    }
}

Response 201:
{
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "users": {
        "profile": {
            "name": "John Doe",
            "title": "Software Developer",
            "is_available": true
        }
    }
}
```

## User Profile Management

### Get User Profile

Users can retrieve their profile information.

```http
GET /api/users/{username}/profile/

Response 200:
{
    "is_available": true,
    "badge": "Available",
    "name": "John Doe",
    "title": "Software Developer",
    "description": "Full-stack developer",
    "social_links": {
        "github": "https://github.com/johndoe",
        "linkedin": "https://linkedin.com/in/johndoe"
    }
}
```

### Update User Profile

Users can update their profile information using the PATCH method.

```http
PATCH /api/users/{username}/profile/

Request Body:
{
    "title": "Lead Developer",
    "is_available": false,
    "badge": "Busy"
}

Response 200:
{
    "name": "John Doe",
    "title": "Lead Developer",
    "is_available": false,
    "badge": "Busy"
}
```

## User Session Management

### Get User Sessions

Users can retrieve their active sessions.

```http
GET /api/session/

Response 200:
[
    {
        "id": 1,
        "session_key": "abc123",
        "created_at": "2025-02-10T15:30:00Z",
        "last_activity": "2025-02-10T15:45:00Z",
        "is_active": true
    }
]
```

### Invalidate User Session

Users can invalidate specific sessions or all sessions except the current one.

```http
DELETE /api/session/

Request Body:
{
    "session_id": 1
}

Response 204: No Content
```

## Security Features

1. **Password Requirements**

   - Minimum length: 10 characters
   - Must include uppercase letters, lowercase letters, numbers, and special characters.

2. **Rate Limiting**

   - Anonymous users: 100 requests/day
   - Authenticated users: 1000 requests/day

3. **Data Protection**
   - HTTPS required in production
   - CSRF protection
   - XSS prevention

## Conclusion

The User Management service provides a robust API for handling user accounts, profiles, and sessions, ensuring a secure and user-friendly experience.
