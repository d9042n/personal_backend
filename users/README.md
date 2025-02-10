# 👥 Users Service

A comprehensive user management system with extended profile capabilities and real-time notifications integration.

## ✨ Features

- 👤 Extended user profiles
- 🔗 Social media integration
- 🎯 Custom badge system
- 🔐 Secure authentication
- 📝 Complete CRUD operations
- 🔌 REST API endpoints
- 📊 Admin interface
- ✅ Comprehensive testing
- 🔄 Real-time notifications

## 🔌 API Endpoints

### Create User

```http
POST /api/users/

{
    "username": "user123",
    "email": "user@example.com",
    "password": "SecurePass123!",
    "users": {
        "profile": {
            "name": "Example User",
            "title": "Software Developer",
            "badge": "Available for hire",
            "github": "https://github.com/username"
        }
    }
}
```

### Get Profile

```http
GET /api/profile/
```

### Update Profile

```http
PUT /api/profile/
{
    "users": {
        "profile": {
            "title": "Senior Developer",
            "badge": "Currently busy"
        }
    }
}
```

## 🧪 Testing

Run the test suite:

```bash
python manage.py test users
```

## 📚 Models

### Users Model

- OneToOne relationship with Django's User model
- Timestamps for creation and updates
- Base for extended user functionality

### Profile Model

- Social media links
- Professional information
- Custom badge system
- Validated URLs

## 🔧 Development

1. Install dependencies
2. Run migrations
3. Create superuser
4. Start development server

## 🤝 Integration

- Seamless integration with Notifications service
- Real-time profile updates
- Extensible architecture

Made with ❤️ for the Personal Website Project
