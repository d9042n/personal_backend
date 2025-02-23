# 📚 Personal Backend Documentation

Welcome to the Personal Backend documentation! This documentation provides detailed information about the backend services, APIs, and integration guides.

## 📑 Table of Contents

1. [Architecture Overview](architecture.md)
2. [Authentication & Authorization](auth.md)
3. [User Management](user-management.md)
4. [Real-time Notifications](notifications.md)
5. [WebSocket Integration](websocket.md)
6. [API Reference](api-reference.md)
7. [Frontend Integration Guide](frontend-integration.md)
8. [Security Guidelines](security.md)
9. [Development Setup](development.md)
10. [Deployment Guide](deployment.md)

## 🚀 Quick Start

1. Clone the repository
2. Copy `.env.example` to `.env.development`
3. Run `make development-up-d`
4. Create superuser: `make development-createsuperuser`

## 📌 Key Features

- 👤 **User Management**

  - Secure authentication with JWT
  - Profile management with social media integration
  - Public/private profile views
  - Role-based access control

- 🔔 **Real-time Notifications**

  - WebSocket-based delivery
  - Multiple notification types
  - Read status tracking
  - Soft deletion support

- 🛠 **Technical Features**
  - REST API with Swagger/ReDoc documentation
  - WebSocket integration
  - Redis caching
  - PostgreSQL with optimized queries

## 🔗 Important Links

- API Documentation: `/swagger/`
- Alternative Docs: `/redoc/`
- Admin Interface: `/admin/`
- Health Check: `/health/`

## 📦 Tech Stack

- Django 4.2+
- Django REST Framework
- Django Channels
- PostgreSQL
- Redis
- JWT Authentication
