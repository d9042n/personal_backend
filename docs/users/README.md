# 👤 Users API Documentation

[![API Status](https://img.shields.io/badge/API-Active-success)](https://github.com/yourusername/personal_backend)
[![JWT](https://img.shields.io/badge/JWT-Authentication-orange)](https://jwt.io/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 📑 Table of Contents

1. [Overview](#overview)
2. [Authentication Endpoints](#authentication-endpoints)
3. [User Management Endpoints](#user-management-endpoints)
4. [Public Endpoints](#public-endpoints)
5. [Session Management](#session-management)
6. [Error Responses](#error-responses)
7. [Rate Limiting](#rate-limiting)

## 🎯 Overview

The Users API provides comprehensive endpoints for user management, authentication, and profile operations. It supports secure user registration, JWT-based authentication, profile management, and session handling across multiple devices.

## 🔐 Authentication Endpoints

### Login

Authenticate a user and receive JWT tokens.

- **URL**: `/api/login/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response** (200 OK):
  ```json
  {
    "data": {
      "access": "string",
      "refresh": "string",
      "user": {
        "username": "string",
        "email": "string",
        "profile": {
          "full_name": "string",
          "bio": "string",
          "created_at": "datetime"
        }
      }
    }
  }
  ```

### Logout

Invalidate the current user session.

- **URL**: `/api/logout/`
- **Method**: `POST`
- **Authentication**: Required
- **Response**: `204 No Content`

### Token Refresh

Obtain a new access token using a refresh token.

- **URL**: `/api/token/refresh/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "refresh": "string"
  }
  ```
- **Response** (200 OK):
  ```json
  {
    "access": "string"
  }
  ```

## 👥 User Management Endpoints

### Create User

Register a new user account.

- **URL**: `/api/users/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string",
    "profile": {
      "full_name": "string",
      "bio": "string"
    }
  }
  ```
- **Response** (201 Created):
  ```json
  {
    "data": {
      "username": "string",
      "email": "string",
      "profile": {
        "full_name": "string",
        "bio": "string",
        "created_at": "datetime"
      }
    }
  }
  ```

### Get User Profile

Retrieve the authenticated user's profile.

- **URL**: `/api/users/{username}/`
- **Method**: `GET`
- **Authentication**: Required
- **Response** (200 OK):
  ```json
  {
    "data": {
      "username": "string",
      "email": "string",
      "profile": {
        "full_name": "string",
        "bio": "string",
        "created_at": "datetime"
      }
    }
  }
  ```

### Update User Profile

Update the authenticated user's profile information.

- **URL**: `/api/users/{username}/profile/`
- **Method**: `PATCH`
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "full_name": "string",
    "bio": "string"
  }
  ```
- **Response** (200 OK):
  ```json
  {
    "data": {
      "full_name": "string",
      "bio": "string",
      "created_at": "datetime"
    }
  }
  ```

### Delete User

Delete the authenticated user's account.

- **URL**: `/api/users/{username}/`
- **Method**: `DELETE`
- **Authentication**: Required
- **Response**: `204 No Content`

## 🌐 Public Endpoints

### Get Public Profile

Retrieve a user's public profile information.

- **URL**: `/api/users/public/{username}/`
- **Method**: `GET`
- **Response** (200 OK):
  ```json
  {
    "data": {
      "username": "string",
      "profile": {
        "full_name": "string",
        "bio": "string"
      }
    }
  }
  ```

## 📱 Session Management

### Get Current Session

Retrieve information about the current user session.

- **URL**: `/api/session/`
- **Method**: `GET`
- **Authentication**: Required
- **Response** (200 OK):
  ```json
  {
    "data": {
      "user": {
        "username": "string",
        "email": "string",
        "profile": {
          "full_name": "string",
          "bio": "string"
        }
      },
      "is_authenticated": true,
      "session_info": {
        "created_at": "datetime",
        "last_active": "datetime",
        "device_info": "string"
      }
    }
  }
  ```

## ⚠️ Error Responses

All endpoints may return the following error responses:

| Status Code | Description  | Common Causes                  |
| ----------- | ------------ | ------------------------------ |
| 400         | Bad Request  | Invalid input data             |
| 401         | Unauthorized | Missing/invalid authentication |
| 403         | Forbidden    | Insufficient permissions       |
| 404         | Not Found    | User not found                 |
| 500         | Server Error | Internal processing error      |

Example error response:

```json
{
  "errors": [
    {
      "field": "username",
      "message": "This username is already taken."
    }
  ]
}
```

## 🚦 Rate Limiting

API endpoints are rate-limited to prevent abuse:

- **Authenticated users**: 100 requests per minute
- **Anonymous users**: 20 requests per minute

When rate limit is exceeded, the API returns a `429 Too Many Requests` response with a `Retry-After` header indicating when to retry.

## 🔒 Security Considerations

- Passwords are securely hashed using Django's password hashing system
- JWT tokens have a limited lifespan (access: 15 minutes, refresh: 7 days)
- Sensitive operations require re-authentication
- All API endpoints use HTTPS in production

---

For more information about the API, refer to the [main documentation](../README.md).
