# Personal Backend API Documentation 📚

[![API Status](https://img.shields.io/badge/API-Active-success)](https://github.com/yourusername/personal_backend)
[![Django](https://img.shields.io/badge/django-4.2-green)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.15-red)](https://www.django-rest-framework.org/)
[![Channels](https://img.shields.io/badge/channels-4.2-purple)](https://channels.readthedocs.io/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Welcome to the comprehensive documentation for the Personal Backend API. This guide provides detailed information about endpoints, authentication mechanisms, and usage guidelines for the implemented features.

## 📑 Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Apps & Modules](#apps--modules)
   - [👤 Users](./users/README.md)
   - [🔔 Notifications](./notifications/README.md)
4. [Common Patterns](#common-patterns)
5. [📊 API Flow Diagrams](./diagrams/README.md)
6. [API Tools](#api-tools)

## 🎯 Overview

The Personal Backend API is a robust platform built using Django REST Framework, offering a comprehensive suite of services including:

- 👤 **User Management**: Complete user authentication, registration, and profile management
- 🔔 **Real-time Notifications**: WebSocket-based notification system using Django Channels
- 🔒 **Secure Authentication**: JWT-based authentication for secure API access
- 📱 **Multi-device Support**: Session management across different devices
- 🚀 **Scalable Architecture**: Designed for high performance and reliability

## 🔐 Authentication

The API implements JWT (JSON Web Token) authentication for secure access control:

### Obtain Token Pair

```http
POST /api/login/
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**

```json
{
  "data": {
    "access": "eyJ0eXAiOiJKV...",
    "refresh": "eyJ0eXAiOiJKV...",
    "user": {
      "username": "your_username",
      "email": "user@example.com",
      "profile": { ... }
    }
  }
}
```

### Use Access Token

```http
GET /api/protected-endpoint/
Authorization: Bearer eyJ0eXAiOiJKV...
```

### Refresh Token

```http
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV..."
}
```

**Response:**

```json
{
  "access": "eyJ0eXAiOiJKV..."
}
```

## 🧩 Apps & Modules

The API is organized into the following modules:

### [👤 Users](./users/README.md)

Complete user management system including:

- Registration and authentication
- Profile management
- Session handling
- Public profile access

### [🔔 Notifications](./notifications/README.md)

Real-time notification system with:

- WebSocket connections for instant updates
- REST endpoints for notification management
- Read/unread status tracking
- Different notification types

## 🔄 Common Patterns

### Request Format

All requests should follow these guidelines:

- Use JSON format for POST/PUT/PATCH requests
- Include proper `Content-Type: application/json` header
- Include `Authorization: Bearer <token>` header for protected endpoints
- Follow RESTful conventions

### Response Format

```json
{
  "data": {}, // Response payload
  "message": "", // Human-readable message (optional)
  "errors": [] // Error details if any
}
```

### 🚦 Error Handling

| Status Code | Description  | Common Causes                  |
| ----------- | ------------ | ------------------------------ |
| 400         | Bad Request  | Invalid input data             |
| 401         | Unauthorized | Missing/invalid authentication |
| 403         | Forbidden    | Insufficient permissions       |
| 404         | Not Found    | Resource doesn't exist         |
| 500         | Server Error | Internal processing error      |

### 📄 Pagination

List endpoints implement cursor-based pagination:

| Parameter   | Description              | Default |
| ----------- | ------------------------ | ------- |
| `cursor`    | Pagination cursor token  | null    |
| `page_size` | Number of items per page | 20      |

## 🛠 API Tools

| Tool         | URL             | Description                   |
| ------------ | --------------- | ----------------------------- |
| Health Check | `/health/`      | API status monitoring         |
| Swagger UI   | `/swagger/`     | Interactive API documentation |
| ReDoc        | `/redoc/`       | Alternative API documentation |
| OpenAPI JSON | `/swagger.json` | Raw OpenAPI specification     |

## 🔌 WebSocket Support

The API supports WebSocket connections for real-time features:

- **Base URL**: `ws://domain/ws/`
- **Authentication**: Via token query parameter
- **Available Channels**:
  - Notifications: `ws://domain/ws/notifications/?token=<your_jwt_token>`

## 🚀 Getting Started

To start using the API:

1. Register a new user account
2. Obtain JWT tokens via login
3. Include the access token in your requests
4. Explore the available endpoints

For detailed examples and code snippets, see the respective module documentation.

---

📝 For detailed information about specific endpoints, please refer to the respective module documentation in the [Apps & Modules](#apps--modules) section.
