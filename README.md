# Personal Backend 🚀

[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/django-4.x-green)](https://www.djangoproject.com/)
[![Docker](https://img.shields.io/badge/docker-ready-blue)](https://www.docker.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A robust and scalable backend service built with Django REST Framework, providing a comprehensive suite of APIs for user management, real-time notifications, and social media integration.

## ✨ Key Features

- 🔐 Secure JWT-based authentication
- 👥 User management system
- 🔔 Real-time notifications
- 🔗 Social media integration
- 📊 API monitoring and analytics
- 🚀 Docker support
- 📚 Comprehensive documentation

## 🛠 Tech Stack

- **Framework:** Django + Django REST Framework
- **Database:** PostgreSQL
- **Caching:** Redis
- **Task Queue:** Celery
- **Documentation:** Swagger/OpenAPI
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

3. **Using Make (recommended)**

   ```bash
   make setup      # Install dependencies and set up environment
   make migrate    # Run database migrations
   make run       # Start development server
   ```

   Or **Manual Setup**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

4. **Using Docker**
   ```bash
   docker-compose up -d
   ```

The API will be available at `http://localhost:8000`

## 📚 Documentation

Comprehensive API documentation is available in the [docs](./docs) directory, including:

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
# or
python manage.py test
```

## 📦 Deployment

The project supports multiple deployment environments:

- Development: `.env.development`
- Staging: `.env.staging`
- Production: `.env.production`

For production deployment instructions, see [Deployment Guide](./docs/deployment.md).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

For detailed information about the API endpoints and usage, please refer to the [API Documentation](./docs/README.md).
