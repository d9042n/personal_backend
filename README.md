# Personal Backend 🚀

[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/django-4.2-green)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.15-red)](https://www.django-rest-framework.org/)
[![Docker](https://img.shields.io/badge/docker-ready-blue)](https://www.docker.com/)
[![Celery](https://img.shields.io/badge/celery-5.4-brightgreen)](https://docs.celeryq.dev/)
[![Channels](https://img.shields.io/badge/channels-4.2-purple)](https://channels.readthedocs.io/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A robust and scalable backend service built with Django REST Framework, providing a comprehensive suite of APIs for user management, real-time notifications, and more. This project follows modern development practices with Docker support for development, staging, and production environments.

## ✨ Key Features

- 🔐 **Secure JWT Authentication**: Complete user authentication flow with JWT tokens
- 👥 **Advanced User Management**: Comprehensive user profiles, authentication, and authorization
- 🔔 **Real-time Notifications**: WebSocket-based notification system using Django Channels
- 🚀 **Multi-environment Support**: Development, staging, and production environments
- 📊 **API Documentation**: Swagger/OpenAPI integration for interactive API documentation
- 🐳 **Docker Integration**: Containerized setup for consistent development and deployment
- 🧪 **Testing**: Comprehensive test suite for all components

## 🛠 Tech Stack

- **Framework:** Django 4.2 + Django REST Framework 3.15
- **Real-time:** Django Channels 4.2 with Redis
- **Database:** PostgreSQL
- **Caching:** Redis
- **Task Queue:** Celery 5.4
- **Documentation:** drf-yasg (Swagger/OpenAPI)
- **Containerization:** Docker & Docker Compose

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Docker and Docker Compose
- Make (optional, but recommended)

### Development Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/personal_backend.git
   cd personal_backend
   ```

2. **Set up environment variables**

   ```bash
   cp .env.development .env
   ```

3. **Using Docker (recommended)**

   ```bash
   make development-build    # Build the Docker containers
   make development-up-d     # Start the services in detached mode
   make development-migrate  # Run database migrations
   ```

   The API will be available at `http://localhost:8000`

4. **Create a superuser**

   ```bash
   make development-createsuperuser
   ```

## 📚 Documentation

Comprehensive API documentation is available in the [docs](./docs) directory:

- [API Reference](./docs/README.md)
- [User Management](./docs/users/README.md)
- [Notifications System](./docs/notifications/README.md)
- [API Flow Diagrams](./docs/diagrams/README.md)

Interactive API documentation is available at:

- Swagger UI: `http://localhost:8000/swagger/`
- ReDoc: `http://localhost:8000/redoc/`

## 🧪 Testing

Run the test suite:

```bash
make test  # Using Make
```

For test coverage:

```bash
make test-coverage
```

## 📦 Deployment

The project supports multiple deployment environments:

- **Development**: `.env.development` - For local development
- **Staging**: `.env.staging` - For testing in a production-like environment
- **Production**: `.env.production` - For production deployment

### Staging Deployment

```bash
make staging-build
make staging-up
make staging-migrate
make staging-collectstatic
```

### Production Deployment

```bash
make production-build
make production-up
make production-migrate
make production-collectstatic
```

## 🛠 Available Make Commands

Run `make help` to see all available commands, including:

- Environment management (build, up, down, logs)
- Database operations (migrations, backup, restore)
- Testing and code quality
- Deployment tasks

## 📋 Project Structure

```
personal_backend/
├── docker/                # Docker configuration for all environments
├── docs/                  # Comprehensive documentation
├── notifications/         # Real-time notification system
├── personal_backend/      # Core Django project settings
├── users/                 # User management and authentication
├── .env.development       # Development environment variables
├── .env.staging           # Staging environment variables
├── .env.production        # Production environment variables
├── Makefile               # Automation commands
├── manage.py              # Django management script
└── requirements.txt       # Python dependencies
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

For detailed information about the API endpoints and usage, please refer to the [API Documentation](./docs/README.md).
