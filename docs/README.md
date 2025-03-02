# Personal Backend API Documentation 📚

[![API Status](https://img.shields.io/badge/API-Active-success)](https://github.com/yourusername/personal_backend)
[![Documentation](https://img.shields.io/badge/docs-up%20to%20date-brightgreen)](https://github.com/yourusername/personal_backend/docs)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Welcome to the comprehensive documentation for the Personal Backend API. This guide provides detailed information about endpoints, authentication mechanisms, and usage guidelines.

## 📑 Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Apps & Modules](#apps)
   - [👤 Users](./users/README.md)
   - [🔔 Notifications](./notifications/README.md)
4. [Common Patterns](#common-patterns)
5. [📊 API Flow Diagrams](./diagrams/README.md)

## 🎯 Overview

The Personal Backend API is a robust platform built using Django REST Framework, offering a comprehensive suite of services including:

- 👤 User management and authentication
- 🔔 Real-time notifications system
- 🔗 Social media integration capabilities
- 🔒 Secure and scalable architecture

## 🔐 Authentication

The API implements JWT (JSON Web Token) authentication for secure access control:

1. **Obtain Token Pair**

   ```http
   POST /api/login/
   ```

2. **Use Access Token**

   ```http
   Authorization: Bearer <your_access_token>
   ```

3. **Refresh Token**
   ```http
   POST /api/token/refresh/
   ```

## 🔄 Common Patterns

### Request Format

All requests should follow these guidelines:

- Use JSON format for POST/PUT/PATCH requests
- Include proper `Content-Type: application/json` header
- Follow RESTful conventions

### Response Format

```json
{
  "data": {}, // Response payload
  "message": "", // Human-readable message
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

---

📝 For detailed information about specific endpoints, please refer to the respective module documentation in the [Apps & Modules](#apps) section.
