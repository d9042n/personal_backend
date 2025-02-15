# 🚀 Staging Deployment Guide

Guide for deploying and maintaining the staging environment using Docker.

## 📋 Environment Overview

| Component | Specification         | Resource Limits      | Port Mapping |
| --------- | --------------------- | -------------------- | ------------ |
| Backend   | Python 3.11, Gunicorn | CPU: 1.0, RAM: 1GB   | 8001 -> 8000 |
| Database  | PostgreSQL 15         | CPU: 0.75, RAM: 1GB  | 5433 -> 5432 |
| Redis     | Redis 7               | CPU: 0.5, RAM: 512MB | 6380 -> 6379 |

## 🚀 Initial Deployment

1. **Setup Environment**

```bash
# Copy staging env file
cp .env.example .env.staging

# Create static and media directories
./docker/staging/setup_static_dirs.sh
```

2. **Configure Environment Variables**

```env
DEBUG=False
SECRET_KEY=<strong-staging-key>
ALLOWED_HOSTS=staging.domain.com,localhost

# Database
DB_NAME=personal_staging
DB_USER=personal_staging
DB_PASSWORD=<strong-password>
DB_HOST=db
DB_PORT=5432

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

3. **Deploy Services**

```bash
# Using Make (recommended)
make staging-build
make staging-up
make staging-migrate
make staging-collectstatic

# Or using Docker Compose directly
docker compose -f docker/staging/docker-compose.yml build
docker compose -f docker/staging/docker-compose.yml up -d
docker compose -f docker/staging/docker-compose.yml exec backend python manage.py migrate
docker compose -f docker/staging/docker-compose.yml exec backend python manage.py collectstatic --noinput
```

## 📝 Maintenance Commands

### Service Management

```bash
# Start services
make staging-up
# or: docker compose -f docker/staging/docker-compose.yml up -d

# Stop services
make staging-down
# or: docker compose -f docker/staging/docker-compose.yml down

# Restart services
make staging-restart
# or: docker compose -f docker/staging/docker-compose.yml restart

# View service status
make staging-ps
# or: docker compose -f docker/staging/docker-compose.yml ps
```

### Logging

```bash
# All services
make staging-logs
# or: docker compose -f docker/staging/docker-compose.yml logs -f

# Specific services
make staging-logs-backend
# or: docker compose -f docker/staging/docker-compose.yml logs backend -f

make staging-logs-db
# or: docker compose -f docker/staging/docker-compose.yml logs db -f

make staging-logs-redis
# or: docker compose -f docker/staging/docker-compose.yml logs redis -f
```

### Database Operations

```bash
# Create backup
make staging-backup-volumes
# or: docker compose -f docker/staging/docker-compose.yml exec db pg_dump -U personal_staging personal_staging > backup_$(date +%Y%m%d_%H%M%S).sql

# Check database connections
make staging-db-connections
# or: docker compose -f docker/staging/docker-compose.yml exec db psql -U personal_staging -c "\x" -c "SELECT * FROM pg_stat_activity;"
```

### Monitoring

```bash
# Health check
make staging-health
# or: docker compose -f docker/staging/docker-compose.yml ps && \
#     curl -f http://localhost:8001/health/ && \
#     docker compose -f docker/staging/docker-compose.yml exec db pg_isready -U personal_staging

# Resource usage
make staging-check-resources
# or: docker stats --no-stream

# Volume permissions
make staging-check-volumes
# or: docker compose -f docker/staging/docker-compose.yml exec backend ls -la /app/staticfiles && \
#     docker compose -f docker/staging/docker-compose.yml exec backend ls -la /app/media
```

## 🔒 Security Features

### Implemented Security Measures

- Non-root user (django) for application container
- Internal bridge network for services
- Health checks for all services
- Resource limits for all containers
- Log rotation (max 3 files of 10MB each)
- Bind-mounted volumes for static/media files
- SSL/TLS ready configuration

### Volume Management

```bash
# Backup volumes
make staging-backup-volumes
# or: mkdir -p backups/staging && \
#     docker run --rm -v personal_postgres_staging:/source -v $(pwd)/backups/staging:/backup \
#     alpine tar czf /backup/postgres_data_$(date +%Y%m%d).tar.gz -C /source . && \
#     docker run --rm -v personal_redis_staging:/source -v $(pwd)/backups/staging:/backup \
#     alpine tar czf /backup/redis_data_$(date +%Y%m%d).tar.gz -C /source .
```

## ⚠️ Emergency Procedures

### Service Recovery

1. Check logs for errors:

```bash
make staging-logs
```

2. Verify resource usage:

```bash
make staging-check-resources
```

3. Restart services if needed:

```bash
make staging-restart
```

### Database Recovery

1. Stop services:

```bash
make staging-down
```

2. Restore from backup:

```bash
make staging-restore file=backup_YYYYMMDD.sql
```

3. Restart services:

```bash
make staging-up
```

## 📊 Resource Specifications

### Container Resources

- Backend:

  - Workers: 2
  - Threads: 2
  - Worker Class: gthread
  - Timeout: 60s
  - Memory: 1GB
  - CPU: 1.0 cores

- Database:

  - Memory: 1GB
  - CPU: 0.75 core
  - Port: 5433

- Redis:
  - Memory: 512MB
  - CPU: 0.5 core
  - Port: 6380

### Volume Mounts

- Static Files: `/var/www/personal/staging/static`
- Media Files: `/var/www/personal/staging/media`
- PostgreSQL Data: `postgres_data_staging`
- Redis Data: `redis_data_staging`

Need urgent assistance? Contact the DevOps team.
