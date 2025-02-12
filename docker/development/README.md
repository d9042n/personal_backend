# 💻 Development Environment Guide

Complete guide for setting up the local development environment for the Personal Backend project.

## 📋 Table of Contents

- [Prerequisites](#-prerequisites)
- [Initial Setup](#-initial-setup)
- [Configuration](#-configuration)
- [Development Server](#-development-server)
- [Development Tools](#-development-tools)
- [Testing](#-testing)
- [Debugging](#-debugging)
- [Troubleshooting](#-troubleshooting)

## 🔧 Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.20+
- Git
- Make (optional, but recommended)
- 1GB RAM minimum
- 5GB disk space

## 📝 Initial Setup

### 1. Clone Repository

```bash
# Clone the repository
git clone https://github.com/yourusername/personal-backend.git
cd personal-backend
```

### 2. Create Development Directories

```bash
# Create required directories
mkdir -p ./data/dev/{static,media,postgres,redis}
mkdir -p ./logs/dev

# Set permissions
chmod 755 ./data/dev/{static,media,postgres,redis}
chmod 755 ./logs/dev
```

## ⚙️ Configuration

### 1. Environment Setup

```bash
# Create development env file
cp .env.example .env.development
```

Edit `.env.development`:

```env
# Django Settings
DEBUG=True
SECRET_KEY=your-dev-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000

# Database Settings
DB_NAME=personal
DB_USER=personal
DB_PASSWORD=devpassword
DB_HOST=db
DB_PORT=5432

# Redis Settings
REDIS_HOST=redis
REDIS_PORT=6379

# Additional Required Settings
POSTGRES_DB=personal
POSTGRES_USER=personal
POSTGRES_PASSWORD=devpassword
```

## 🚀 Development Server

### 1. Start Development Environment

```bash
# Build images
make development-build

# Start services
make development-up

# View logs
make development-logs
```

### 2. Initialize Database

```bash
# Run migrations
make development-migrate

# Create superuser
make development-createsuperuser
```

## 🛠 Development Tools

### Django Management

```bash
# Django shell
make development-shell

# Create new migrations
make development-makemigrations

# Apply migrations
make development-migrate
```

### Database Access

```bash
# Check database status
make development-db-status

# View connections
make development-db-connections

# Direct database access
docker compose -f docker/development/docker-compose.yml exec db psql -U personal
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
make test-coverage
```

### Test Database

```bash
# Access test database
docker compose -f docker/development/docker-compose.yml exec db psql -U personal personal_test
```

## 🔍 Monitoring

### Health Checks

```bash
# Check service health
make development-health

# Check volumes
make development-check-volumes

# Monitor resources
make development-check-resources
```

### Logs

```bash
# View all logs
make development-logs

# Follow specific service logs
docker compose -f docker/development/docker-compose.yml logs -f backend
docker compose -f docker/development/docker-compose.yml logs -f db
```

## 🐛 Debugging

### Django Debug Toolbar

- Available at http://localhost:8000/debug/
- SQL query analysis
- Request/response information
- Cache statistics

### Hot Reload

Code changes are automatically detected for:

- Python files
- Templates
- Static files

### VS Code Debugging

1. Install Python extension
2. Add configuration:

```json
{
  "name": "Django Docker",
  "type": "python",
  "request": "attach",
  "port": 5678,
  "host": "localhost",
  "pathMappings": [
    {
      "localRoot": "${workspaceFolder}",
      "remoteRoot": "/app"
    }
  ]
}
```

## 🔧 Resource Limits

Development environment uses minimal resources:

```yaml
Backend:
  CPU: 0.50
  Memory: 512M

Database:
  CPU: 0.50
  Memory: 512M

Redis:
  CPU: 0.50
  Memory: 512M
```

## 🔍 Troubleshooting

### Common Issues

1. **Port Conflicts**

```bash
# Check ports in use
sudo lsof -i :8000
sudo lsof -i :5432

# Change ports in docker-compose.yml if needed
```

2. **Database Issues**

```bash
# Reset database
docker compose -f docker/development/docker-compose.yml down -v
make development-up
make development-migrate
```

3. **Permission Issues**

```bash
# Fix permissions
sudo chown -R $USER:$USER ./data/dev
sudo chmod -R 755 ./data/dev
```

4. **Cache Issues**

```bash
# Clear Redis cache
docker compose -f docker/development/docker-compose.yml exec redis redis-cli FLUSHALL
```

## 📚 Development Best Practices

1. **Code Quality**

   - Run tests before committing
   - Use black for formatting
   - Follow PEP 8 guidelines

2. **Database**

   - Use migrations for schema changes
   - Don't modify production data in development

3. **Security**

   - Never commit .env files
   - Use development-specific credentials
   - Keep DEBUG=True only in development

4. **Performance**
   - Monitor query performance
   - Use Django Debug Toolbar
   - Profile slow operations
