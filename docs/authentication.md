# JWT Authentication Documentation

## Overview

This document describes the comprehensive authentication system implemented in the backend API. The system uses JWT (JSON Web Token) for authentication along with advanced session management features for enhanced security and user experience.

### Key Features

- JWT-based authentication with access and refresh tokens
- Multi-device session management with location tracking
- Automatic session extension for active users (every 15 minutes)
- IP-based location tracking and device detection
- Periodic cleanup of expired sessions (every 30 minutes)
- Rate limiting protection

## Authentication Flow

1. **Login**: User provides credentials (username/email and password)
2. **Token Generation**: Server validates credentials and returns access and refresh tokens
3. **Session Creation**: Server creates a new session with device and location information
4. **Request Authorization**: Client includes access token in requests
5. **Session Management**: Server tracks and manages active sessions
6. **Token Refresh**: Client uses refresh token to get new access token when needed
7. **Session Extension**: Active sessions are automatically extended
8. **Logout**: Client blacklists tokens and ends session

## API Endpoints

### Login

- **URL**: `/api/login/`
- **Method**: `POST`
- **Rate Limit**: 100 requests per day (anonymous)
- **Request Body**:
  ```json
  {
    "username_or_email": "string",
    "password": "string"
  }
  ```
- **Success Response** (200 OK):
  ```json
  {
    "refresh": "string",
    "access": "string",
    "user": {
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
  }
  ```
- **Error Response** (401 Unauthorized):
  ```json
  {
    "error": "Invalid credentials"
  }
  ```

### Refresh Token

- **URL**: `/api/token/refresh/`
- **Method**: `POST`
- **Rate Limit**: 1000 requests per day (authenticated)
- **Request Body**:
  ```json
  {
    "refresh": "string"
  }
  ```
- **Success Response** (200 OK):
  ```json
  {
    "access": "string"
  }
  ```
- **Error Response** (401 Unauthorized):
  ```json
  {
    "detail": "Token is invalid or expired"
  }
  ```

### Logout

- **URL**: `/api/logout/`
- **Method**: `POST`
- **Headers**: `Authorization: Bearer <access_token>`
- **Rate Limit**: 1000 requests per day (authenticated)
- **Request Body**:
  ```json
  {
    "refresh_token": "string"
  }
  ```
- **Success Response** (200 OK):
  ```json
  {
    "detail": "Successfully logged out."
  }
  ```

### Session Management

- **URL**: `/api/session/`
- **Method**: `GET`, `DELETE`
- **Headers**: `Authorization: Bearer <access_token>`
- **Rate Limit**: 1000 requests per day (authenticated)
- **GET Response** (200 OK):
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
- **DELETE Request Body** (for specific session):
  ```json
  {
    "session_id": 1
  }
  ```
- **DELETE Request Body** (for all other sessions):
  ```json
  {
    "all_except_current": true
  }
  ```

## Frontend Implementation Guide

### 1. Setting Up Authentication Headers

```javascript
// Add this interceptor to your HTTP client (e.g., axios)
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || "http://localhost:8000/api",
  timeout: 5000, // 5 seconds timeout
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);
```

### 2. Login Implementation with Session Management

```javascript
async function login(username_or_email, password) {
  try {
    const response = await api.post("/login/", {
      username_or_email,
      password,
    });

    const { access, refresh, user } = response.data;

    // Store tokens and user data
    localStorage.setItem("access_token", access);
    localStorage.setItem("refresh_token", refresh);
    localStorage.setItem("user", JSON.stringify(user));

    // Set up session monitoring
    startSessionMonitoring();

    return user;
  } catch (error) {
    handleAuthError(error);
    throw error;
  }
}

function startSessionMonitoring() {
  // Check session status every minute
  const interval = setInterval(async () => {
    try {
      const response = await api.get("/session/");
      const sessions = response.data;

      if (sessions.length === 0) {
        clearInterval(interval);
        await logout();
        return;
      }

      const currentSession = sessions[0];
      if (currentSession.time_until_expiry < 300) {
        // 5 minutes
        await refreshToken();
      }
    } catch (error) {
      console.error("Session monitoring error:", error);
    }
  }, 60000);

  // Store interval ID for cleanup
  localStorage.setItem("session_monitor", interval);
}
```

### 3. Enhanced Token Refresh Implementation

```javascript
async function refreshToken() {
  try {
    const refresh = localStorage.getItem("refresh_token");
    if (!refresh) {
      throw new Error("No refresh token available");
    }

    const response = await api.post("/token/refresh/", {
      refresh,
    });

    const { access } = response.data;
    localStorage.setItem("access_token", access);

    return access;
  } catch (error) {
    // If refresh fails, log out the user
    await logout();
    throw new Error("Session expired. Please login again.");
  }
}

// Add this interceptor to handle token expiration
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const newToken = await refreshToken();
        originalRequest.headers.Authorization = `Bearer ${newToken}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Clear session monitoring
        const monitorInterval = localStorage.getItem("session_monitor");
        if (monitorInterval) clearInterval(monitorInterval);

        // Redirect to login page
        window.location.href = "/login";
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);
```

### 4. Comprehensive Logout Implementation

```javascript
async function logout() {
  try {
    const refresh_token = localStorage.getItem("refresh_token");

    if (refresh_token) {
      await api.post("/logout/", {
        refresh_token,
      });
    }
  } catch (error) {
    console.error("Logout error:", error);
  } finally {
    // Clear session monitoring
    const monitorInterval = localStorage.getItem("session_monitor");
    if (monitorInterval) clearInterval(monitorInterval);

    // Clear all auth-related data
    clearAuthData();

    // Redirect to login page
    window.location.href = "/login";
  }
}

function clearAuthData() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("user");
  localStorage.removeItem("session_monitor");
}
```

## Security Features

### 1. Token Configuration

- Access tokens expire after 30 minutes
- Refresh tokens expire after 7 days
- Tokens are rotated on refresh
- Tokens are blacklisted after rotation
- JWT uses HS256 algorithm
- Automatic token refresh for active sessions

### 2. Session Management

- Database-backed session storage
- Location-based session tracking
- Device type detection
- Automatic session extension (15-minute intervals)
- Periodic cleanup of expired sessions (30-minute intervals)
- Multiple session support with device tracking

### 3. Security Headers

- HTTPS required in production
- HSTS enabled (1 year, including subdomains)
- XSS protection enabled
- Content type sniffing protection
- X-Frame-Options set to DENY
- Strict CORS policy
- Secure cookie configuration

### 4. Rate Limiting

- Anonymous users: 100 requests per day
- Authenticated users: 1000 requests per day
- Applies to all API endpoints

## Error Handling

### Common Error Scenarios

1. **Invalid Credentials** (401):

   ```json
   {
     "error": "Invalid username/email or password"
   }
   ```

2. **Token Expired** (401):

   ```json
   {
     "detail": "Token has expired"
   }
   ```

3. **Invalid Token** (401):

   ```json
   {
     "detail": "Token is invalid or malformed"
   }
   ```

4. **Session Expired** (401):

   ```json
   {
     "detail": "Session expired."
   }
   ```

5. **Rate Limit Exceeded** (429):
   ```json
   {
     "detail": "Request was throttled"
   }
   ```

### Error Handling Implementation

```javascript
function handleAuthError(error) {
  const errorMessage =
    error.response?.data?.error || error.response?.data?.detail;

  switch (error.response?.status) {
    case 401:
      if (errorMessage.includes("Token has expired")) {
        return handleTokenExpiration();
      } else if (errorMessage.includes("Invalid credentials")) {
        return handleInvalidCredentials();
      }
      return handleUnauthorized();

    case 403:
      return handleForbidden();

    case 429:
      return handleRateLimitExceeded();

    default:
      return handleGenericError(errorMessage);
  }
}

function handleRateLimitExceeded() {
  return {
    error: "Too many requests. Please try again later.",
    retryAfter: parseInt(error.response.headers["retry-after"] || "60"),
  };
}
```

## Testing Guide

### 1. Testing Authentication Flow

```javascript
describe("Authentication Flow", () => {
  test("successful login", async () => {
    const credentials = {
      username_or_email: "test@example.com",
      password: "testpass123",
    };

    const response = await login(credentials);
    expect(response.user).toBeDefined();
    expect(localStorage.getItem("access_token")).toBeTruthy();
  });

  test("session monitoring", async () => {
    const sessions = await api.get("/session/");
    expect(sessions.data.length).toBeGreaterThan(0);
    expect(sessions.data[0].is_active).toBe(true);
  });
});
```

## Best Practices

1. **Token Storage**

   - Use secure storage mechanisms
   - Clear tokens on logout
   - Implement automatic cleanup

2. **Session Management**

   - Monitor active sessions
   - Implement session timeout
   - Track suspicious activity

3. **Error Handling**

   - Implement comprehensive error handling
   - Show user-friendly error messages
   - Log errors for debugging

4. **Security**

   - Use HTTPS in production
   - Implement proper CORS
   - Regular security audits

5. **Testing**
   - Test all authentication flows
   - Test error scenarios
   - Regular security testing
