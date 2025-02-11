# 🌟 User Profile API

A clean, RESTful API for user profile management with a focus on simplicity and security.

## 🎯 Core Features

- 🔓 Public profile viewing & registration
- 👤 User management
- ✏️ Profile customization
- 🔒 Secure authentication
- 🔗 Social media integration
- 📱 Real-time updates

## 📚 API Documentation

### Public Endpoints (No Authentication Required)

#### View Public Profile

```http
GET /api/public/profile/{username}/
```

Returns public profile information for any user.

**Response** `200 OK`

```json
{
  "username": "johndoe",
  "profile": {
    "is_available": true,
    "name": "John Doe",
    "title": "Software Developer",
    "badge": "Available",
    "description": "Full-stack developer",
    "github": "https://github.com/johndoe"
  }
}
```

#### Register New Account

```http
POST /api/users/

{
    "username": "newuser",
    "email": "user@example.com",
    "password": "secure_password",
    "users": {
        "profile": {
            "is_available": true,
            "name": "New User",
            "title": "Developer"
        }
    }
}
```

### Protected Endpoints (Authentication Required\*)

\*Note: Authentication requirement controlled by API_REQUIRE_AUTH setting

#### View Full Profile

```http
GET /api/users/{username}/
```

Returns complete user information including private fields.

#### Update Profile

```http
PATCH /api/users/{username}/

{
    "users": {
        "profile": {
            "title": "Senior Developer",
            "badge": "Available"
        }
    }
}
```

#### Delete Account

```http
DELETE /api/users/{username}/
```

## 🔒 Security Features

- Public access limited to:
  - Viewing public profiles (/public/profile/{username}/)
  - User registration (/users/ POST)
- Protected operations require:
  - Authentication (when API_REQUIRE_AUTH is True)
  - Authorization (can only modify own profile)
- Rate limiting:
  - Public endpoints: 100 requests/day
  - Authenticated users: 1000 requests/day
- Password security:
  - Minimum length: 10 characters
  - Complexity requirements enforced
  - Hashing using Django's default hasher
- Email verification required
- CORS protection enabled
- XSS protection
- Content type sniffing protection
- SSL/HTTPS enforcement in production

## 🚀 Best Practices

1. **RESTful Design**

   - Clear public/protected endpoint separation
   - Consistent URL structure (/public/profile/, /users/)
   - Proper HTTP methods (GET, POST, PATCH, DELETE)
   - Meaningful status codes

2. **Security First**

   - Secure by default
   - Rate limiting
   - Input validation
   - Clear authentication rules

3. **Clean Architecture**
   - Separation of concerns
   - Modular design
   - Clear documentation
   - Consistent error handling

## 💻 Development Guide

1. **Setup Environment**

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
```

2. **Run Tests**

```bash
python manage.py test users
```

## 🔌 Integration Features

- WebSocket notifications for profile updates
- Social media URL validation
- Real-time event handling
- Extensible profile data

## 📝 API Design Notes

- Clear separation between public and protected endpoints
- Consistent response formats
- Comprehensive error handling
- Rate limiting for security
- Cached public endpoints
- Supports partial updates

## 🤝 Related Services

- Integrates with Notification system
- Supports WebSocket connections
- Extensible for additional features

## 🔌 Profile Features

- 🎯 Availability Control
  - Toggle badge visibility with `is_available`
  - Automatic notification on status change
  - Real-time frontend updates

---

📖 For detailed API documentation, visit `/swagger/` or `/redoc/`

Made with ❤️ for the Personal Website Project
