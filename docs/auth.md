# 🔒 Authentication & Authorization

## Overview

The Personal Backend uses token-based authentication to secure API endpoints. This section outlines the authentication flow, token management, and authorization mechanisms.

## Authentication Flow

1. **User Login**

   - Users authenticate by sending their credentials (username and password) to the login endpoint.
   - On successful authentication, the server responds with access and refresh tokens.

   ### Login Endpoint

   ```http
   POST /api/login/

   Request Body:
   {
       "username": "johndoe",
       "password": "SecurePass123!"
   }

   Response 200:
   {
       "refresh": "refresh_token",
       "access": "access_token",
       "user": {
           "id": 1,
           "username": "johndoe",
           "email": "john@example.com"
       }
   }
   ```

2. **Token Management**

   - **Access Token**: Short-lived token used for authenticating requests.
   - **Refresh Token**: Long-lived token used to obtain new access tokens without re-authentication.

   ### Token Expiration

   - Access tokens expire after a specified duration (e.g., 30 minutes).
   - Refresh tokens can be used to obtain new access tokens until they expire (e.g., 1 day).

3. **User Logout**

   - Users can log out, which invalidates the current session and refresh token.

   ### Logout Endpoint

   ```http
   POST /api/logout/

   Response 200:
   {
       "detail": "Successfully logged out."
   }
   ```

## Authorization

- **Role-Based Access Control**: The application implements role-based access control to restrict access to certain endpoints based on user roles (e.g., admin, user).
- **Permission Classes**: Django REST Framework's permission classes are used to enforce access control.

### Example Permission Classes

```python
from rest_framework.permissions import IsAuthenticated, AllowAny

class UserViewSet(viewsets.ViewSet):
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]
```

## Security Best Practices

1. **Use HTTPS**: Always use HTTPS to encrypt data in transit.
2. **Secure Token Storage**: Store tokens securely on the client-side (e.g., in memory or secure storage).
3. **Implement Rate Limiting**: Protect against brute-force attacks by limiting login attempts.
4. **Use CSRF Protection**: Implement CSRF protection for state-changing requests.

## Conclusion

This authentication and authorization framework ensures that only authenticated users can access protected resources while maintaining a secure environment for user data.
