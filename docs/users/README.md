# Users API Documentation

## Overview

The Users API provides endpoints for user management, authentication, and profile operations. It supports user registration, login, profile management, and session handling.

## Authentication Endpoints

### Login

- **URL**: `/api/login/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response**:
  ```json
  {
    "data": {
      "access": "string",
      "refresh": "string",
      "user": {
        "username": "string",
        "email": "string",
        "profile": {}
      }
    }
  }
  ```

### Logout

- **URL**: `/api/logout/`
- **Method**: `POST`
- **Authentication**: Required
- **Response**: `204 No Content`

### Token Refresh

- **URL**: `/api/token/refresh/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "refresh": "string"
  }
  ```
- **Response**:
  ```json
  {
    "access": "string"
  }
  ```

## User Management Endpoints

### Create User

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
- **Response**: `201 Created`

### Get User Profile

- **URL**: `/api/users/{username}/`
- **Method**: `GET`
- **Authentication**: Required
- **Response**:
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
- **Response**: `200 OK`

### Delete User

- **URL**: `/api/users/{username}/`
- **Method**: `DELETE`
- **Authentication**: Required
- **Response**: `204 No Content`

## Public Endpoints

### Get Public Profile

- **URL**: `/api/users/public/{username}/`
- **Method**: `GET`
- **Response**:
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

## Session Management

### Get Current Session

- **URL**: `/api/session/`
- **Method**: `GET`
- **Authentication**: Required
- **Response**:
  ```json
  {
    "data": {
      "user": {
        "username": "string",
        "email": "string",
        "profile": {}
      },
      "is_authenticated": true
    }
  }
  ```

## Error Responses

All endpoints may return the following error responses:

- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: User not found
- `500 Internal Server Error`: Server-side error

## Rate Limiting

API endpoints are rate-limited to:

- 100 requests per minute for authenticated users
- 20 requests per minute for anonymous users
