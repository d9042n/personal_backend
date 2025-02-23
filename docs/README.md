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

## 📊 Diagrams

- [User Registration Flow](diagrams/flows/user_registration_flow.md)
- [User Login Flow](diagrams/flows/user_login_flow.md)
- [User Logout Flow](diagrams/flows/user_logout_flow.md)
- [Edit User Profile Flow](diagrams/flows/edit_user_profile_flow.md)
- [Manage User Sessions Flow](diagrams/flows/manage_user_sessions_flow.md)
- [Real-time Notifications Flow](diagrams/flows/real_time_notifications_flow.md)
- [Mark Notifications as Read Flow](diagrams/flows/mark_notifications_as_read_flow.md)
- [Delete Notifications Flow](diagrams/flows/delete_notifications_flow.md)

## 📈 Sequence Diagrams

- [User Registration Sequence](diagrams/sequences/user_registration_sequence.md)
- [User Login Sequence](diagrams/sequences/user_login_sequence.md)
- [User Logout Sequence](diagrams/sequences/user_logout_sequence.md)
- [Edit User Profile Sequence](diagrams/sequences/edit_user_profile_sequence.md)
- [Manage User Sessions Sequence](diagrams/sequences/manage_user_sessions_sequence.md)
- [Real-time Notifications Sequence](diagrams/sequences/real_time_notifications_sequence.md)
- [Mark Notifications as Read Sequence](diagrams/sequences/mark_notifications_as_read_sequence.md)
- [Delete Notifications Sequence](diagrams/sequences/delete_notifications_sequence.md)
