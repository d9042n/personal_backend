# 👤 User Profile Management Service

A comprehensive RESTful API service for user profile management, focusing on security, extensibility, and real-time updates.

## ✨ Features

- 🔐 **Secure Authentication and Authorization**: Token-based authentication with support for JWT.
- 👥 **Public and Private Profile Views**: Users can view public profiles and manage their own private profiles.
- 🚀 **Real-time Profile Updates**: Integration with a notification service for real-time updates.
- 🔄 **Seamless Integration with Notifications**: Users receive notifications for profile updates and session management.
- 📱 **Social Media Profile Linking**: Users can link their social media accounts to their profiles.
- 🎨 **Customizable User Badges**: Users can set their availability status with customizable badges.
- 🔍 **Advanced Profile Search**: Search for users based on various criteria.
- 📊 **Activity Tracking**: Track user activity and session management.

## 🔌 REST API Endpoints

### Public Endpoints

| Method | Endpoint                       | Description         | Auth Required |
| ------ | ------------------------------ | ------------------- | ------------- |
| GET    | `/api/users/public/{username}` | View public profile | No            |
| POST   | `/api/users`                   | Register new user   | No            |

### Protected Endpoints

| Method | Endpoint                        | Description                | Auth Required |
| ------ | ------------------------------- | -------------------------- | ------------- |
| GET    | `/api/users/{username}`         | Get user details           | Yes           |
| PUT    | `/api/users/{username}`         | Update user                | Yes           |
| PATCH  | `/api/users/{username}`         | Partially update user      | Yes           |
| DELETE | `/api/users/{username}`         | Delete user                | Yes           |
| GET    | `/api/users/{username}/profile` | Get profile                | Yes           |
| PATCH  | `/api/users/{username}/profile` | Update profile             | Yes           |
| POST   | `/api/login/`                   | User Login                 | No            |
| POST   | `/api/logout/`                  | User Logout                | Yes           |
| GET    | `/api/session/`                 | Get user sessions          | Yes           |
| DELETE | `/api/session/`                 | Invalidate user session(s) | Yes           |

## 📝 API Examples

### View Public Profile

```http
GET /api/users/public/johndoe

Response 200:
{
    "username": "johndoe",
    "profile": {
        "name": "John Doe",
        "title": "Senior Developer",
        "badge": "Available",
        "is_available": true,
        "description": "Full-stack developer with 5 years experience",
        "social_links": {
            "github": "https://github.com/johndoe",
            "linkedin": "https://linkedin.com/in/johndoe",
            "twitter": "https://twitter.com/johndoe",
            "facebook": "https://facebook.com/johndoe",
            "leetcode": "https://leetcode.com/johndoe",
            "hackerrank": "https://hackerrank.com/johndoe",
            "medium": "https://medium.com/@johndoe",
            "stackoverflow": "https://stackoverflow.com/users/123/johndoe",
            "portfolio": "https://johndoe.dev",
            "youtube": "https://youtube.com/@johndoe",
            "devto": "https://dev.to/johndoe"
        }
    }
}
```

### Create User

```http
POST /api/users

Request:
{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "users": {
        "profile": {
            "name": "John Doe",
            "title": "Senior Developer",
            "is_available": true,
            "description": "Full-stack developer",
            "github": "https://github.com/johndoe",
            "linkedin": "https://linkedin.com/in/johndoe",
            "twitter": "https://twitter.com/johndoe",
            "facebook": "https://facebook.com/johndoe",
            "leetcode": "https://leetcode.com/johndoe",
            "hackerrank": "https://hackerrank.com/johndoe",
            "medium": "https://medium.com/@johndoe",
            "stackoverflow": "https://stackoverflow.com/users/123/johndoe",
            "portfolio": "https://johndoe.dev",
            "youtube": "https://youtube.com/@johndoe",
            "devto": "https://dev.to/johndoe"
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
            "title": "Senior Developer",
            "is_available": true,
            "social_links": {
                "github": "https://github.com/johndoe",
                "linkedin": "https://linkedin.com/in/johndoe",
                "twitter": "https://twitter.com/johndoe",
                "facebook": "https://facebook.com/johndoe",
                "leetcode": "https://leetcode.com/johndoe",
                "hackerrank": "https://hackerrank.com/johndoe",
                "medium": "https://medium.com/@johndoe",
                "stackoverflow": "https://stackoverflow.com/users/123/johndoe",
                "portfolio": "https://johndoe.dev",
                "youtube": "https://youtube.com/@johndoe",
                "devto": "https://dev.to/johndoe"
            }
        }
    }
}
```

### Update Profile

```http
PATCH /api/users/johndoe/profile

Request:
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

## 🔒 Security Features

### Authentication

- Token-based authentication
- Session support
- OAuth2 integration (optional)

### Password Requirements

- Minimum length: 10 characters
- Must include:
  - Uppercase letters
  - Lowercase letters
  - Numbers
  - Special characters

### Rate Limiting

- Anonymous: 100 requests/day
- Authenticated: 1000 requests/day

### Data Protection

- HTTPS required in production
- CORS protection
- XSS prevention
- CSRF tokens
- SQL injection prevention

## 🔄 Real-time Updates

The service integrates with the Notifications service to provide real-time profile updates:

```javascript
// WebSocket connection for real-time updates
const socket = new WebSocket("ws://your-domain/ws/notifications/");

socket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.type === "profile_update") {
    updateProfileUI(data.profile_update);
  }
};
```

## 🛠️ Development

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### Testing

```bash
# Run all tests
python manage.py test users

# Run specific test
python manage.py test users.tests.UserAPITest
```

### Code Quality

```bash
# Run linting
flake8 users

# Run type checking
mypy users
```

## 📚 Documentation

Detailed API documentation is available at:

- Swagger UI: `/swagger/`
- ReDoc: `/redoc/`

## 🔧 Configuration

Environment variables:

| Variable           | Description             | Default    |
| ------------------ | ----------------------- | ---------- |
| `API_REQUIRE_AUTH` | Require authentication  | `True`     |
| `PASSWORD_MIN_LEN` | Minimum password length | `10`       |
| `RATE_LIMIT_ANON`  | Anonymous rate limit    | `100/day`  |
| `RATE_LIMIT_USER`  | User rate limit         | `1000/day` |

## 📦 Dependencies

- Django 4.2+
- Django REST Framework
- Channels (WebSocket)
- PostgreSQL
- Redis (WebSocket)

---

Made with ❤️ for the Personal Website Project
