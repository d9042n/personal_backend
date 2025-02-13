# 🚀 Production Deployment Guide

Guide for deploying and maintaining the production environment using Docker.

## 📋 Environment Overview

| Component | Specification         | Resource Limits    |
| --------- | --------------------- | ------------------ |
| Backend   | Python 3.11, Gunicorn | CPU: 2.0, RAM: 2GB |
| Database  | PostgreSQL 15         | CPU: 1.0, RAM: 2GB |
| Redis     | Redis 7               | CPU: 1.0, RAM: 1GB |
| Port      | 8000 (Behind Nginx)   | -                  |

## 🚀 Initial Deployment

1. **Setup Environment**

```bash
# Copy production env file
cp .env.example .env.production

# Create static and media directories
./docker/production/setup_static_dirs.sh
```

2. **Configure Environment Variables**

```env
DEBUG=False
SECRET_KEY=<strong-production-key>
ALLOWED_HOSTS=your-domain.com

# Database
DB_NAME=personal_production
DB_USER=personal_production
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
make production-build
make production-up
make production-migrate
make production-collectstatic

# Or using Docker Compose directly
docker compose -f docker/production/docker-compose.yml build
docker compose -f docker/production/docker-compose.yml up -d
docker compose -f docker/production/docker-compose.yml exec backend python manage.py migrate
docker compose -f docker/production/docker-compose.yml exec backend python manage.py collectstatic --noinput
```

## 📝 Maintenance Commands

### Service Management

```bash
# Start services
make production-up
# or: docker compose -f docker/production/docker-compose.yml up -d

# Stop services
make production-down
# or: docker compose -f docker/production/docker-compose.yml down

# Restart services
make production-restart
# or: docker compose -f docker/production/docker-compose.yml restart

# View service status
make production-ps
# or: docker compose -f docker/production/docker-compose.yml ps
```

### Logging

```bash
# All services
make production-logs
# or: docker compose -f docker/production/docker-compose.yml logs -f

# Specific services
make production-logs-backend
# or: docker compose -f docker/production/docker-compose.yml logs backend -f

make production-logs-db
# or: docker compose -f docker/production/docker-compose.yml logs db -f

make production-logs-redis
# or: docker compose -f docker/production/docker-compose.yml logs redis -f
```

### Database Operations

```bash
# Create backup
make db-backup
# or: docker compose -f docker/production/docker-compose.yml exec db pg_dump -U personal_production personal_production > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore from backup
make db-restore file=backup_file.sql
# or: docker compose -f docker/production/docker-compose.yml exec -T db psql -U personal_production personal_production < backup_file.sql

# Check database connections
make production-db-connections
# or: docker compose -f docker/production/docker-compose.yml exec db psql -U personal_production -c "\x" -c "SELECT * FROM pg_stat_activity;"
```

### Monitoring

```bash
# Health check
make production-health
# or: docker compose -f docker/production/docker-compose.yml ps && \
#     curl -f http://localhost:8000/health/ && \
#     docker compose -f docker/production/docker-compose.yml exec db pg_isready -U personal_production

# Resource usage
make production-check-resources
# or: docker stats --no-stream

# Volume permissions
make production-check-volumes
# or: docker compose -f docker/production/docker-compose.yml exec backend ls -la /app/staticfiles && \
#     docker compose -f docker/production/docker-compose.yml exec backend ls -la /app/media
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
make production-backup-volumes
# or: mkdir -p backups && \
#     docker run --rm -v personal_postgres_prod:/source -v $(pwd)/backups:/backup \
#     alpine tar czf /backup/postgres_data_$(date +%Y%m%d).tar.gz -C /source . && \
#     docker run --rm -v personal_redis_prod:/source -v $(pwd)/backups:/backup \
#     alpine tar czf /backup/redis_data_$(date +%Y%m%d).tar.gz -C /source .
```

## ⚠️ Emergency Procedures

### Service Recovery

1. Check logs for errors:

```bash
make production-logs
```

2. Verify resource usage:

```bash
make production-check-resources
```

3. Restart services if needed:

```bash
make production-restart
```

### Database Recovery

1. Stop services:

```bash
make production-down
```

2. Restore from backup:

```bash
make db-restore file=backup_YYYYMMDD.sql
```

3. Restart services:

```bash
make production-up
```

## 📊 Resource Specifications

### Container Resources

- Backend:

  - Workers: 4
  - Threads: 2
  - Worker Class: gthread
  - Timeout: 120s
  - Memory: 2GB
  - CPU: 2.0 cores

- Database:

  - Memory: 2GB
  - CPU: 1.0 core
  - Port: 5432

- Redis:
  - Memory: 1GB
  - CPU: 1.0 core
  - Port: 6379

### Volume Mounts

- Static Files: `/var/www/personal/static`
- Media Files: `/var/www/personal/media`
- PostgreSQL Data: `postgres_data_prod`
- Redis Data: `redis_data_prod`

Need urgent assistance? Contact the SRE team immediately.
