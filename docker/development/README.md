# 💻 Local Development Guide

Quick guide to start developing the Personal Backend project locally.

## 🚀 Quick Start

1. **Setup Project**

```bash
# Clone repository
git clone https://github.com/yourusername/personal-backend.git
cd personal-backend

# Copy environment file
cp .env.example .env.development
```

2. **Configure Environment**
   Edit `.env.development`:

```env
DEBUG=True
SECRET_KEY=dev-secret-key
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
```

3. **Start Development**

```bash
# Start all services
make development-up

# Run migrations
make development-migrate

# Create admin user (optional)
make development-createsuperuser
```

4. **Access Your Project**

- Main: http://localhost:8002
- Admin: http://localhost:8002/admin
- API Docs: http://localhost:8002/api/docs

## 📝 Development Commands

### Daily Use

```bash
# Start/Stop
make development-up      # Start services
make development-down    # Stop services
make development-logs    # View logs

# Database
make development-migrate         # Apply migrations
make development-makemigrations  # Create migrations
make development-shell          # Django shell

# Testing
make test               # Run tests
```

### Database Connection

```python
DATABASES = {
    'default': {
        'HOST': 'localhost',
        'PORT': '5432',
        'NAME': 'personal',
        'USER': 'personal',
        'PASSWORD': 'devpassword',
    }
}
```

## 🔄 Development Features

### Auto-Reload

- Python code changes reload automatically
- Templates update on refresh
- Static files served automatically

### Debugging

- Django Debug Toolbar at /debug/
- Python debugger enabled
- Full error pages

### Local Services

- Database: PostgreSQL at localhost:5432
- Redis: localhost:6379
- Backend: localhost:8002

## ❗ Common Issues

### Port Already in Use

```bash
# Check ports
sudo lsof -i :8002    # Backend
sudo lsof -i :5432    # Database
sudo lsof -i :6379    # Redis

# Stop services
make development-down
```

### Database Reset

```bash
# Full reset
make development-down
rm -rf ./data/dev/postgres/*
make development-up
make development-migrate
```

### Cache Clear

```bash
# Clear Redis
make development-shell
>>> from django.core.cache import cache
>>> cache.clear()
```

Need help? Check our [Contributing Guide](../../CONTRIBUTING.md) or ask the team!
