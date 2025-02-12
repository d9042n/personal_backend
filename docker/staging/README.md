# 🚀 Staging Deployment Guide

Complete guide for deploying the Personal Backend project in staging environment.

## 📋 Table of Contents

- [Prerequisites](#-prerequisites)
- [Initial Setup](#-initial-setup)
- [Configuration](#-configuration)
- [Deployment](#-deployment)
- [Post-Deployment](#-post-deployment)
- [Maintenance](#-maintenance)
- [Monitoring](#-monitoring)
- [Backup & Recovery](#-backup--recovery)
- [Troubleshooting](#-troubleshooting)

## 🔧 Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.20+
- 2GB RAM minimum
- 10GB disk space
- Staging domain (optional)
- Nginx reverse proxy configured

## 📝 Initial Setup

### 1. Create Required Directories

```bash
# Create project structure
mkdir -p /opt/personal-backend-staging/{data,backups,logs}
cd /opt/personal-backend-staging

# Create data subdirectories
mkdir -p data/{static,media,postgres,redis}

# Set permissions
chmod 755 data/{static,media,postgres,redis}
chmod 755 {backups,logs}
```

### 2. Clone Repository

```bash
git clone https://github.com/yourusername/personal-backend.git
cd personal-backend
```

## ⚙️ Configuration

### 1. Environment Setup

```bash
# Create staging env file
cp .env.example .env.staging
```

Edit `.env.staging`:

```env
# Django Settings
DEBUG=False
SECRET_KEY=your-staging-secret-key
ALLOWED_HOSTS=staging.your-domain.com,localhost
CORS_ALLOWED_ORIGINS=https://staging.your-domain.com

# Database Settings
DB_NAME=personal_staging
DB_USER=personal_staging
DB_PASSWORD=staging-password
DB_HOST=db
DB_PORT=5432

# Redis Settings
REDIS_HOST=redis
REDIS_PORT=6379

# Security Settings
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Additional Required Settings
POSTGRES_DB=personal_staging
POSTGRES_USER=personal_staging
POSTGRES_PASSWORD=staging-password
```

## 🚀 Deployment

### 1. Build and Start Services

```bash
# Build images
make staging-build

# Start services
make staging-up

# Verify services are running
make staging-ps
```

### 2. Initialize Database

```bash
# Run migrations
make staging-migrate

# Create superuser
docker compose -f docker/staging/docker-compose.yml exec backend python manage.py createsuperuser
```

### 3. Static Files

```bash
# Collect static files
make staging-collectstatic
```

## ✅ Post-Deployment

### 1. Verify Deployment

```bash
# Check service health
make staging-health

# Test endpoints
curl http://localhost:8000/health/
```

### 2. Monitor Logs

```bash
# View all logs
make staging-logs

# View specific service logs
make staging-logs-backend
make staging-logs-db
make staging-logs-redis
```

## 🛠 Maintenance

### Regular Updates

```bash
# Pull latest changes
git pull origin develop

# Rebuild and restart
make staging-build
make staging-up

# Run migrations if needed
make staging-migrate
```

### Database Maintenance

```bash
# Create backup
make staging-backup-volumes

# Check database status
make staging-db-status
```

## 📊 Monitoring

### Health Checks

```bash
# Check all services
make staging-health

# Check volumes
make staging-check-volumes

# Monitor resources
make staging-check-resources
```

### Performance Monitoring

```bash
# Check database connections
make staging-db-connections

# View resource usage
docker stats
```

## 💾 Backup & Recovery

### Automated Backups

```bash
# Volume backups
make staging-backup-volumes
```

### Recovery

```bash
# Restore volumes
docker run --rm -v backup.tar.gz:/backup -v volume_name:/data alpine tar xzf /backup
```

## 🔍 Troubleshooting

### Common Issues

1. **Service Won't Start**

```bash
# Using Make (Recommended)
make staging-health

# Manual checks
docker compose -f docker/staging/docker-compose.yml ps
docker compose -f docker/staging/docker-compose.yml logs
```

2. **Database Connection Issues**

```bash
# Using Make (Recommended)
make staging-db-status
make staging-db-connections

# Manual checks
docker compose -f docker/staging/docker-compose.yml logs db
docker compose -f docker/staging/docker-compose.yml exec db pg_isready -U personal_staging
```

3. **Volume Permission Issues**

```bash
# Using Make (Recommended)
make staging-check-volumes

# Manual checks
docker compose -f docker/staging/docker-compose.yml exec backend ls -la /app/staticfiles
docker compose -f docker/staging/docker-compose.yml exec backend ls -la /app/media
```

## 📈 Performance Tuning

### Resource Allocation

```yaml
Backend:
  CPU: 1.0
  Memory: 1G

Database:
  CPU: 0.75
  Memory: 1G

Redis:
  CPU: 0.50
  Memory: 512M
```

### Gunicorn Settings

- Workers: `2` (half of production)
- Threads: `2`
- Worker Class: `gthread`
- Timeout: `60` seconds

### Database Optimization

```bash
# Check current connections
make staging-db-status

# Monitor query performance
make staging-db-connections
```
