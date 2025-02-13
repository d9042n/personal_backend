# 👤 Users Service

A comprehensive user management system providing profile management, authentication, and real-time updates through a RESTful API.

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Models](#-models)
- [API Reference](#-api-reference)
- [Authentication](#-authentication)
- [Validation](#-validation)
- [Integration](#-integration)
- [Development](#-development)
- [Testing](#-testing)

## ✨ Features

- 🔐 Secure user authentication
- 👤 Extensible user profiles
- 🌐 Social media integration
- 🔄 Real-time profile updates
- 🛡️ Role-based access control
- 📊 Advanced data validation
- 🔍 Optimized database queries
- 📱 WebSocket notifications
- 🌍 Public/private profile separation

## 🏗 Architecture

### Core Components

1. **Models**

   - `Users`: Extended user information
   - `Profile`: Professional and social details
   - Optimized database indexes
   - Automatic profile creation

2. **Views**

   - Public profile access
   - Protected user operations
   - Swagger documentation
   - Rate limiting

3. **Services**

   - User creation
   - Profile management
   - Transaction handling

4. **Validators**
   - Social media URL validation
   - Custom field validation
   - Input sanitization

## 📦 Models

### Users Model

```python
class Users(models.Model):
    user = models.OneToOneField(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['-created_at']),
        ]
```

### Profile Model

```python
class Profile(models.Model):
    users = models.OneToOneField(Users)
    is_available = models.BooleanField(default=True)
    badge = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.TextField()
    github = models.URLField(validators=[validate_github_url])
    linkedin = models.URLField(validators=[validate_linkedin_url])
    twitter = models.URLField(validators=[validate_twitter_url])

    class Meta:
        indexes = [
            models.Index(fields=['users']),
            models.Index(fields=['badge']),
            models.Index(fields=['is_available']),
        ]
```

## 🔌 API Reference

### Public Endpoints

```http
GET /api/public/profile/{username}/
```

Returns public profile information:

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

```http
POST /api/users/
```

Register new user account:

```json
{
  "username": "newuser",
  "email": "user@example.com",
  "password": "secure_password",
  "users": {
    "profile": {
      "is_available": true,
      "name": "New User",
      "title": "Developer",
      "description": "Full-stack developer",
      "github": "https://github.com/newuser",
      "linkedin": "https://linkedin.com/in/newuser",
      "twitter": "https://twitter.com/newuser"
    }
  }
}
```

Response `201 Created`:

```json
{
  "id": 1,
  "username": "newuser",
  "email": "user@example.com",
  "users": {
    "profile": {
      "is_available": true,
      "name": "New User",
      "title": "Developer",
      "badge": "",
      "description": "Full-stack developer",
      "github": "https://github.com/newuser",
      "linkedin": "https://linkedin.com/in/newuser",
      "twitter": "https://twitter.com/newuser"
    },
    "created_at": "2024-03-15T10:30:00Z",
    "updated_at": "2024-03-15T10:30:00Z"
  }
}
```

### Protected Endpoints

```http
GET /api/users/{username}/
PATCH /api/users/{username}/
DELETE /api/users/{username}/
```

Notes:

- Authentication requirement controlled by `API_REQUIRE_AUTH` setting
- Protected endpoints require authentication when `API_REQUIRE_AUTH=True`
- Registration endpoint is always public
- Rate limiting applies to all endpoints

## 🔒 Authentication

### Configuration

```python
# settings.py
API_REQUIRE_AUTH = True  # Enable/disable authentication requirement
```

### Rate Limiting

- Anonymous: 100 requests/day
- Authenticated: 1000 requests/day

## ✅ Validation

### Social Media URLs

```python
GITHUB_URL_PATTERN = r'^https?://(?:www\.)?github\.com/[\w-]+/?$'
LINKEDIN_URL_PATTERN = r'^https?://(?:www\.)?linkedin\.com/in/[\w-]+/?$'
TWITTER_URL_PATTERN = r'^https?://(?:www\.)?twitter\.com/[\w-]+/?$'
```

### Profile Badges

```python
BADGE_CHOICES = [
    ('available', 'Available for hire'),
    ('busy', 'Currently busy'),
    ('offline', 'Not available'),
]
```

## 🔌 Integration

### WebSocket Notifications

```python
@receiver(post_save, sender=Profile)
def notify_profile_update(sender, instance, created, **kwargs):
    if not created:
        NotificationService.create_notification(
            recipient=instance.users.user,
            notification_type=NotificationTypes.PROFILE_UPDATE,
            message='Your profile has been updated',
            content_object=instance
        )
```

## 🧪 Testing

### Running Tests

```bash
# Run all user tests
python manage.py test users

# Run specific test case
python manage.py test users.tests.UserAPITest
```

### Test Coverage

```bash
coverage run manage.py test users
coverage report
```

## 🔧 Development

### Creating Users

```python
from users.services import UserService

user = UserService.create_user(
    username='johndoe',
    email='john@example.com',
    password='secure_password',
    profile_data={
        'title': 'Software Developer',
        'badge': 'available'
    }
)
```

### Updating Profiles

```python
UserService.update_user_profile(
    user=user,
    profile_data={
        'title': 'Senior Developer',
        'is_available': True
    }
)
```

## 🔒 Security Features

1. **Authentication**

   - Configurable API authentication
   - Role-based access control
   - Rate limiting

2. **Data Protection**

   - Input validation
   - URL sanitization
   - Field-level permissions

3. **Performance**
   - Optimized queries
   - Database indexes
   - Cached responses

## 📚 Additional Resources

- [Django Authentication](https://docs.djangoproject.com/en/stable/topics/auth/)
- [DRF Permissions](https://www.django-rest-framework.org/api-guide/permissions/)
- [WebSocket Integration](../notifications/README.md)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Write tests for new features
4. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Made with ❤️ by the Personal Website Team
