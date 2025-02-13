# 🚀 Personal Backend

A robust and scalable backend service providing user management, real-time notifications, and profile handling through a RESTful API and WebSocket integration.

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Getting Started](#-getting-started)
- [Environment Setup](#-environment-setup)
- [API Documentation](#-api-documentation)
- [Development](#-development)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Contributing](#-contributing)

## ✨ Features

- 👤 **User Management**

  - Secure authentication
  - Profile management with social media integration
  - Public/private profile separation
  - Role-based access control
  - Real-time profile updates

- 🔔 **Real-time Notifications**

  - WebSocket-based delivery
  - Multiple notification types (Profile Update, Mention, System)
  - Read status tracking
  - Soft deletion support
  - Generic relations to any model

- 🛠 **Technical Features**
  - REST API with Swagger/ReDoc documentation
  - WebSocket integration with Django Channels
  - Redis caching and channel layers
  - PostgreSQL with optimized queries
  - Docker multi-stage builds
  - Environment-specific configurations

## 🏗 Architecture

### Core Components

1. **Users Service**

   - Extended Django User model
   - Profile management with social validation
   - Real-time updates via WebSocket
   - Rate limiting and permissions
   - Swagger-documented endpoints

2. **Notifications Service**

   - WebSocket notifications with Django Channels
   - Generic relations for flexibility
   - Redis channel layer for scaling
   - Asynchronous message handling
   - Soft deletion support

3. **Infrastructure**
   - Multi-stage Docker builds
   - PostgreSQL with optimized indexes
   - Redis for caching and channels
   - Nginx reverse proxy (Production)
   - Health checks for all services

### Environment Specifications

| Environment | Backend                  | Database                   | Redis                | Ports            |
| ----------- | ------------------------ | -------------------------- | -------------------- | ---------------- |
| Development | Django (CPU: 0.5, 512MB) | PostgreSQL 15 (0.5, 512MB) | Redis 7 (0.5, 512MB) | 8002, 5434, 6381 |
| Staging     | Gunicorn (CPU: 1.0, 1GB) | PostgreSQL 15 (0.75, 1GB)  | Redis 7 (0.5, 512MB) | 8001, 5433, 6380 |
| Production  | Gunicorn (CPU: 2.0, 2GB) | PostgreSQL 15 (1.0, 2GB)   | Redis 7 (1.0, 1GB)   | 8000, 5432, 6379 |

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose
- Make (optional, but recommended)
- Git

### Quick Start

```bash
# Clone repository
git clone https://github.com/yourusername/personal-backend.git
cd personal-backend

# Development setup
cp .env.example .env.development
make development-up-d

# Create superuser
make development-createsuperuser

# Access services:
- API: http://localhost:8002
- Admin: http://localhost:8002/admin/
- API Docs: http://localhost:8002/swagger/
- ReDoc: http://localhost:8002/redoc/
- Health Check: http://localhost:8002/health/
```

### Available Make Commands

```bash
# Development
make development-build      # Build containers
make development-up-d      # Start services
make development-down      # Stop services
make development-logs      # View logs
make development-shell     # Access Django shell
make development-migrate   # Run migrations

# Database
make development-db-status        # Check DB status
make development-db-connections   # View connections
make db-backup                   # Create backup
make db-restore file=backup.sql  # Restore backup

# Monitoring
make development-health           # Check health
make development-check-resources  # Monitor resources
make development-check-volumes    # Check volumes
```

## 📚 API Documentation

### Interactive Documentation

- Swagger UI: `/swagger/` - Interactive API documentation
- ReDoc: `/redoc/` - Alternative API documentation
- Django Admin: `/admin/` - Database administration
- Health Check: `/health/` - Service health status

### User Management

```http
# Public Endpoints
GET /api/public/profile/{username}/   # View public profile
POST /api/users/                      # Register new user

# Protected Endpoints
GET /api/users/{username}/            # Get user profile
PATCH /api/users/{username}/          # Update profile
DELETE /api/users/{username}/         # Delete account
```

Example Profile Response:

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

### Notifications

```http
GET /api/notifications/                    # List notifications
POST /api/notifications/{id}/mark-read/    # Mark as read
POST /api/notifications/mark-all-read/     # Mark all as read
DELETE /api/notifications/{id}/delete/     # Delete notification
```

### WebSocket Integration

```javascript
// Connect to notification WebSocket
const socket = new WebSocket("ws://your-domain/ws/notifications/");

// Handle messages
socket.onmessage = (event) => {
  const notification = JSON.parse(event.data);
  console.log("New notification:", notification);
};

// Handle connection
socket.onopen = () => {
  console.log("Connected to notifications");
};

socket.onerror = (error) => {
  console.error("WebSocket error:", error);
};
```

## 🔧 Development

### Environment Variables

```env
# Core Settings
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=personal
DB_USER=personal
DB_PASSWORD=devpassword
DB_HOST=db
DB_PORT=5432

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# API Settings
API_REQUIRE_AUTH=True
```

### Database Indexes

The project includes optimized indexes for:

- User profiles
- Notification queries
- Social media fields
- Timestamp-based queries

### Health Checks

All services implement health checks:

- Backend: HTTP endpoint check every 30s
- Database: PostgreSQL readiness check every 10s
- Redis: Connection check every 10s

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test users
python manage.py test notifications

# Test coverage
coverage run manage.py test
coverage report
```

## 🔒 Security Features

1. **Authentication**

   - Configurable API authentication
   - Role-based access control
   - Rate limiting (100/day anonymous, 1000/day authenticated)
   - Secure session handling
   - Social media URL validation

2. **Data Protection**

   - Input validation and sanitization
   - Field-level permissions
   - SSL/TLS support
   - CORS protection
   - XSS prevention

3. **Infrastructure**
   - Non-root container users
   - Resource limits and monitoring
   - Automated health checks
   - Regular backups
   - Log rotation

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Write tests for new features
4. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📚 Additional Resources

- [Development Guide](docker/development/README.md)
- [Staging Guide](docker/staging/README.md)
- [Production Guide](docker/production/README.md)
- [Docker Guide](docker/README.md)
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Django Channels](https://channels.readthedocs.io/)

## 🆘 Troubleshooting

### Common Issues

1. **Port Conflicts**

```bash
# Check ports on Linux/MacOS
sudo lsof -i :8002
sudo lsof -i :5434
sudo lsof -i :6381
```

2. **Database Reset**

```bash
make development-down
docker volume rm development_postgres_data_dev
make development-up-d
make development-migrate
```

3. **Permission Issues**

```bash
# Check volume permissions
make development-check-volumes
```

### Getting Help

- Check the [FAQ](docs/faq.md)
- Review the [Troubleshooting Guide](docs/troubleshooting.md)
- Submit an issue on GitHub
- Contact the development team

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Made with ❤️ by the Personal Website Team
