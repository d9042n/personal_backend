# 🐳 Docker Configuration Guide

This directory contains Docker configurations for different environments of the Personal Backend project.

## 📋 Directory Structure

```
docker/
├── development/        # Development environment
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── README.md
├── staging/           # Staging environment
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── README.md
├── production/        # Production environment
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── README.md
└── README.md         # This file
```

## 🌐 Environment Specifications

### Development Environment

| Component | Specification        | Resource Limits      | Port Mapping |
| --------- | -------------------- | -------------------- | ------------ |
| Backend   | Python 3.11 (Django) | CPU: 0.5, RAM: 512MB | 8002 -> 8000 |
| Database  | PostgreSQL 15        | CPU: 0.5, RAM: 512MB | 5434 -> 5432 |
| Redis     | Redis 7              | CPU: 0.5, RAM: 512MB | 6381 -> 6379 |

### Staging Environment

| Component | Specification          | Resource Limits      | Port Mapping |
| --------- | ---------------------- | -------------------- | ------------ |
| Backend   | Python 3.11 (Gunicorn) | CPU: 1.0, RAM: 1GB   | 8001 -> 8000 |
| Database  | PostgreSQL 15          | CPU: 0.75, RAM: 1GB  | 5433 -> 5432 |
| Redis     | Redis 7                | CPU: 0.5, RAM: 512MB | 6380 -> 6379 |

### Production Environment

| Component | Specification          | Resource Limits    | Port Mapping |
| --------- | ---------------------- | ------------------ | ------------ |
| Backend   | Python 3.11 (Gunicorn) | CPU: 2.0, RAM: 2GB | 8000 -> 8000 |
| Database  | PostgreSQL 15          | CPU: 1.0, RAM: 2GB | 5432 -> 5432 |
| Redis     | Redis 7                | CPU: 1.0, RAM: 1GB | 6379 -> 6379 |

## 🚀 Quick Start

### Using Make Commands (Recommended)

```bash
# Development Environment
make development-build
make development-up-d
# Access at http://localhost:8002

# Staging Environment
make staging-build
make staging-up
# Access at http://localhost:8001

# Production Environment
make production-build
make production-up
# Access at http://localhost:8000
```

### Using Docker Compose Directly

```bash
# Development
docker compose -f docker/development/docker-compose.yml up -d

# Staging
docker compose -f docker/staging/docker-compose.yml up -d

# Production
docker compose -f docker/production/docker-compose.yml up -d
```

## 🔧 Environment Features

### Development

- Hot reload enabled
- Debug mode ON
- Volume mounts for live code changes
- Direct database access
- Minimal resource limits
- Django development server

### Staging

- Gunicorn with 2 workers
- Debug mode OFF
- Moderate resource limits
- Health checks enabled
- Log rotation
- Static file serving

### Production

- Gunicorn with 4 workers
- Maximum security measures
- Higher resource limits
- Health checks
- Log rotation
- Static/media file optimization
- Non-root user execution

## 📝 Common Operations

### Service Management

```bash
# Start services
make [env]-up-d

# Stop services
make [env]-down

# View logs
make [env]-logs

# Check health
make [env]-health
```

### Database Operations

```bash
# Run migrations
make [env]-migrate

# Create backup
make db-backup  # Production only

# Check status
make [env]-db-status
```

### Monitoring

```bash
# Check resources
make [env]-check-resources

# View volume permissions
make [env]-check-volumes

# Check service health
make [env]-health
```

## 🔒 Security Features

### Common Security Measures

- Health checks for all services
- Resource limits
- Log rotation (max 3 files of 10MB each)
- Internal Docker networks

### Production/Staging Additional Security

- Non-root user (django)
- SSL/TLS ready
- Bind-mounted volumes
- Limited port exposure
- Gunicorn worker configuration

## 📦 Volume Management

### Development

- Local volume mounts for hot reload
- Python packages volume for dependency caching

### Staging/Production

- Persistent PostgreSQL data
- Persistent Redis data
- Bind-mounted static files
- Bind-mounted media files

## 🔍 Health Checks

All environments implement health checks:

- Backend: Every 30s via HTTP endpoint
- Database: Every 10s via pg_isready
- Redis: Every 10s via ping

## 📚 Documentation

Detailed environment-specific guides:

- [Development Guide](development/README.md)
- [Staging Guide](staging/README.md)
- [Production Guide](production/README.md)

## ⚠️ Important Notes

1. **Environment Files**

   - Copy appropriate .env.example for each environment
   - Never commit .env files
   - Use strong passwords in staging/production

2. **Resource Scaling**

   - Development: Minimal resources for local development
   - Staging: Moderate resources for testing
   - Production: Full resources for live deployment

3. **Port Conflicts**

   - Each environment uses different ports to avoid conflicts
   - Check port availability before starting services

4. **Data Persistence**
   - Development: Local volumes for easy reset
   - Staging/Production: Named volumes for persistence

Need help? Check the environment-specific README files or contact the DevOps team.
