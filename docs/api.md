# API Documentation

## Overview

This document provides comprehensive documentation for the backend API endpoints. The API uses JWT authentication and supports various operations for user management, profiles, and sessions.

## Base URL

```
http://localhost:8000/api/
```

## Authentication

The API uses JWT (JSON Web Token) authentication. Most endpoints require authentication via Bearer token in the Authorization header:

```
Authorization: Bearer <access_token>
```

For detailed authentication documentation, please see [Authentication Documentation](authentication.md).

## Rate Limiting

- Anonymous endpoints: 100 requests per day
- Authenticated endpoints: 1000 requests per day

## API Endpoints

### Public Endpoints

#### Get Public Profile

Retrieve public profile information for any user.

- **URL**: `/users/public/{username}/`
- **Method**: `GET`
- **Auth required**: No
- **Rate limit**: 100 requests per day (anonymous)
- **Success Response** (200 OK):
  ```json
  {
    "username": "string",
    "profile": {
      "name": "string",
      "title": "string",
      "description": "string",
      "badge": "string",
      "is_available": true,
      "social_links": {
        "github": "string",
        "linkedin": "string",
        "twitter": "string",
        "facebook": "string",
        "leetcode": "string",
        "hackerrank": "string",
        "medium": "string",
        "stackoverflow": "string",
        "portfolio": "string",
        "youtube": "string",
        "devto": "string"
      }
    }
  }
  ```
- **Error Response** (404 Not Found):
  ```json
  {
    "detail": "User not found"
  }
  ```

### User Management

#### Create User

Create a new user account.

- **URL**: `/users/`
- **Method**: `POST`
- **Auth required**: No
- **Rate limit**: 100 requests per day (anonymous)
- **Request Body**:
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string",
    "first_name": "string",
    "last_name": "string"
  }
  ```
- **Success Response** (201 Created):
  ```json
  {
    "id": 1,
    "username": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string"
  }
  ```
- **Error Response** (400 Bad Request):
  ```json
  {
    "username": ["This field is required"],
    "email": ["Enter a valid email address"],
    "password": ["Password must be at least 8 characters long"]
  }
  ```

#### Get User Details

Retrieve details for a specific user.

- **URL**: `/users/{username}/`
- **Method**: `GET`
- **Auth required**: Yes
- **Rate limit**: 1000 requests per day (authenticated)
- **Success Response** (200 OK):
  ```json
  {
    "id": 1,
    "username": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "users": {
      "profile": {
        "is_available": true,
        "badge": "string",
        "name": "string",
        "title": "string",
        "description": "string",
        "social_links": {}
      }
    }
  }
  ```
- **Error Response** (404 Not Found):
  ```json
  {
    "detail": "User not found"
  }
  ```

#### Update User

Update a user's information.

- **URL**: `/users/{username}/`
- **Method**: `PUT`
- **Auth required**: Yes
- **Rate limit**: 1000 requests per day (authenticated)
- **Request Body**:
  ```json
  {
    "username": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "password": "string"
  }
  ```
- **Success Response** (200 OK):
  ```json
  {
    "id": 1,
    "username": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string"
  }
  ```
- **Error Responses**:
  - 400 Bad Request: Invalid data
  - 403 Forbidden: Permission denied
  - 404 Not Found: User not found

#### Partially Update User

Update specific fields of a user's information.

- **URL**: `/users/{username}/`
- **Method**: `PATCH`
- **Auth required**: Yes
- **Rate limit**: 1000 requests per day (authenticated)
- **Request Body**:
  ```json
  {
    "username": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "password": "string",
    "users": {
      "profile": {
        "is_available": true,
        "badge": "string",
        "name": "string",
        "title": "string",
        "description": "string",
        "social_links": {
          "github": "string",
          "linkedin": "string",
          "twitter": "string",
          "facebook": "string",
          "leetcode": "string",
          "hackerrank": "string",
          "medium": "string",
          "stackoverflow": "string",
          "portfolio": "string",
          "youtube": "string",
          "devto": "string"
        }
      }
    }
  }
  ```
- **Success Response** (200 OK):
  ```json
  {
    "id": 1,
    "username": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "users": {
      "profile": {
        "is_available": true,
        "badge": "string",
        "name": "string",
        "title": "string",
        "description": "string",
        "social_links": {}
      }
    }
  }
  ```
- **Error Responses**:
  - 400 Bad Request: Invalid data provided
  - 401 Unauthorized: Authentication required
  - 403 Forbidden: Permission denied
  - 404 Not Found: User not found

#### Delete User

Delete a user account.

- **URL**: `/users/{username}/`
- **Method**: `DELETE`
- **Auth required**: Yes
- **Rate limit**: 1000 requests per day (authenticated)
- **Success Response** (204 No Content)
- **Error Responses**:
  - 403 Forbidden: Permission denied
  - 404 Not Found: User not found

### Profile Management

#### Get User Profile

Retrieve a user's profile information.

- **URL**: `/users/{username}/profile/`
- **Method**: `GET`
- **Auth required**: Yes
- **Rate limit**: 1000 requests per day (authenticated)
- **Success Response** (200 OK):
  ```json
  {
    "username": "string",
    "profile": {
      "is_available": true,
      "badge": "string",
      "name": "string",
      "title": "string",
      "description": "string",
      "social_links": {
        "github": "string",
        "linkedin": "string",
        "twitter": "string",
        "facebook": "string",
        "leetcode": "string",
        "hackerrank": "string",
        "medium": "string",
        "stackoverflow": "string",
        "portfolio": "string",
        "youtube": "string",
        "devto": "string"
      }
    }
  }
  ```
- **Error Response** (404 Not Found):
  ```json
  {
    "detail": "User not found"
  }
  ```

#### Update Profile

Update a user's profile information.

- **URL**: `/users/{username}/profile/`
- **Method**: `PATCH`
- **Auth required**: Yes
- **Rate limit**: 1000 requests per day (authenticated)
- **Request Body**:
  ```json
  {
    "is_available": true,
    "badge": "string",
    "name": "string",
    "title": "string",
    "description": "string",
    "github": "string",
    "linkedin": "string",
    "twitter": "string",
    "facebook": "string",
    "leetcode": "string",
    "hackerrank": "string",
    "medium": "string",
    "stackoverflow": "string",
    "portfolio": "string",
    "youtube": "string",
    "devto": "string"
  }
  ```
- **Success Response** (200 OK):
  ```json
  {
    "is_available": true,
    "badge": "string",
    "name": "string",
    "title": "string",
    "description": "string",
    "social_links": {
      "github": "string",
      "linkedin": "string",
      "twitter": "string",
      "facebook": "string",
      "leetcode": "string",
      "hackerrank": "string",
      "medium": "string",
      "stackoverflow": "string",
      "portfolio": "string",
      "youtube": "string",
      "devto": "string"
    }
  }
  ```
- **Error Responses**:
  - 400 Bad Request: Invalid data
  - 403 Forbidden: Permission denied
  - 404 Not Found: User not found

### Session Management

#### Get User Sessions

Retrieve all active sessions for the authenticated user.

- **URL**: `/session/`
- **Method**: `GET`
- **Auth required**: Yes
- **Rate limit**: 1000 requests per day (authenticated)
- **Success Response** (200 OK):
  ```json
  [
    {
      "id": 1,
      "session_key": "string",
      "created_at": "datetime",
      "last_activity": "datetime",
      "ip_address": "string",
      "user_agent": "string",
      "device_type": "string",
      "location": "string",
      "is_active": true,
      "expires_at": "datetime",
      "duration": 0,
      "time_until_expiry": 0
    }
  ]
  ```
- **Success Response** (204 No Content):
  When no active sessions are found.

#### Invalidate Sessions

Invalidate specific session or all sessions except current.

- **URL**: `/session/`
- **Method**: `DELETE`
- **Auth required**: Yes
- **Rate limit**: 1000 requests per day (authenticated)
- **Request Body** (for specific session):
  ```json
  {
    "session_id": 1
  }
  ```
- **Request Body** (for all other sessions):
  ```json
  {
    "all_except_current": true
  }
  ```
- **Success Response** (204 No Content)
- **Error Responses**:
  - 400 Bad Request: Invalid request parameters
  - 404 Not Found: Session not found

## Error Codes

The API uses standard HTTP status codes:

- 200: OK - Request successful
- 201: Created - Resource created successfully
- 204: No Content - Request successful, no content to return
- 400: Bad Request - Invalid request data
- 401: Unauthorized - Authentication required
- 403: Forbidden - Permission denied
- 404: Not Found - Resource not found
- 429: Too Many Requests - Rate limit exceeded
- 500: Internal Server Error - Server error

## Rate Limiting Headers

Rate limit information is included in response headers:

```
X-RateLimit-Limit: <requests_per_day>
X-RateLimit-Remaining: <remaining_requests>
X-RateLimit-Reset: <reset_time>
```

## Best Practices

1. Always include the Authorization header for authenticated endpoints
2. Handle rate limiting by checking response headers
3. Implement token refresh logic for long-running applications
4. Store sensitive data (like tokens) securely
5. Implement proper error handling for all API calls
