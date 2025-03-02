# Personal Backend API Documentation

This documentation provides comprehensive information about the Personal Backend API endpoints, authentication, and usage guidelines.

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Apps](#apps)
   - [Users](./users/README.md)
   - [Notifications](./notifications/README.md)
4. [Common Patterns](#common-patterns)
5. [API Flow Diagrams](./diagrams/README.md)

## Overview

The Personal Backend API is built using Django REST Framework and provides endpoints for:

- User management and authentication
- Real-time notifications
- Social media integration

## Authentication

The API uses JWT (JSON Web Token) authentication. To access protected endpoints:

1. Obtain a token pair by logging in at `/api/login/`
2. Use the access token in the Authorization header: `Bearer <token>`
3. Refresh expired tokens at `/api/token/refresh/`

## Common Patterns

### Request Format

- All POST/PUT/PATCH requests should send data in JSON format
- Set Content-Type header to `application/json`

### Response Format

All responses follow a standard format:

```json
{
  "data": {}, // Response data (if successful)
  "message": "string", // Human-readable message
  "errors": [] // Array of errors (if any)
}
```

### Error Handling

- 400: Bad Request - Invalid input
- 401: Unauthorized - Missing or invalid authentication
- 403: Forbidden - Insufficient permissions
- 404: Not Found - Resource doesn't exist
- 500: Server Error - Internal processing error

### Pagination

List endpoints use cursor-based pagination with the following parameters:

- `cursor`: Pagination cursor
- `page_size`: Number of items per page (default: 20)

## API Status

Check API health at `/health/`

## API Documentation UI

- Swagger UI: `/swagger/`
- ReDoc: `/redoc/`
- OpenAPI Schema: `/swagger.json`
