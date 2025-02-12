# 🚀 Production Deployment Guide

Complete guide for deploying the Personal Backend project in production environment.

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
- 4GB RAM minimum
- 20GB disk space
- Domain with SSL certificate
- Nginx reverse proxy configured

## 📝 Initial Setup

### 1. Create Required Directories

```bash
# Create project structure
mkdir -p /opt/personal-backend/{data,backups,logs}
cd /opt/personal-backend

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
# Create production env file
cp .env.example .env.production
```

Edit `.env.production`:

```env
# Django Settings
DEBUG=False
SECRET_KEY=your-secure-production-key
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
CORS_ALLOWED_ORIGINS=https://your-domain.com

# Database Settings
DB_NAME=personal_production
DB_USER=personal_production
DB_PASSWORD=strong-production-password
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
POSTGRES_DB=personal_production
POSTGRES_USER=personal_production
POSTGRES_PASSWORD=strong-production-password
```

## 🚀 Deployment

### 1. Build and Start Services

```bash
# Build images
make production-build

# Start services
make production-up

# Verify services are running
make production-ps
```

### 2. Initialize Database

```bash
# Run migrations
make production-migrate

# Create superuser
docker compose -f docker/production/docker-compose.yml exec backend python manage.py createsuperuser
```

### 3. Static Files

```bash
# Collect static files
make production-collectstatic
```

## ✅ Post-Deployment

### 1. Verify Deployment

```bash
# Check service health
make production-health

# Test endpoints
curl https://your-domain.com/health/
```

### 2. Monitor Logs

```bash
# View all logs
make production-logs

# View specific service logs
make production-logs-backend
make production-logs-db
make production-logs-redis
```

## 🛠 Maintenance

### Regular Updates

```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
make production-build
make production-up

# Run migrations if needed
make production-migrate
```

### Database Maintenance

```bash
# Create backup
make db-backup

# Check database status
make production-db-status
```

## 📊 Monitoring

### Health Checks

```bash
# Check all services
make production-health

# Check volumes
make production-check-volumes

# Monitor resources
make production-check-resources
```

### Performance Monitoring

```bash
# Check database connections
make production-db-connections

# View resource usage
docker stats
```

## 💾 Backup & Recovery

### Automated Backups

```bash
# Database backup
make db-backup

# Volume backups
make production-backup-volumes
```

### Recovery

```bash
# Restore database
make db-restore file=backup_20240101.sql

# Restore volumes
docker run --rm -v backup.tar.gz:/backup -v volume_name:/data alpine tar xzf /backup
```

## 🔍 Troubleshooting

### Common Issues

1. **Service Won't Start**

```bash
# Using Make (Recommended)
make production-health

# Manual checks
docker compose -f docker/production/docker-compose.yml ps
docker compose -f docker/production/docker-compose.yml logs
curl http://localhost:8000/health/
```

2. **Database Connection Issues**

```bash
# Using Make (Recommended)
make production-db-status
make production-db-connections

# Manual checks
docker compose -f docker/production/docker-compose.yml logs db
docker compose -f docker/production/docker-compose.yml exec db pg_isready -U personal_production
```

3. **Volume Permission Issues**

```bash
# Using Make (Recommended)
make production-check-volumes

# Manual checks
docker compose -f docker/production/docker-compose.yml exec backend ls -la /app/staticfiles
docker compose -f docker/production/docker-compose.yml exec backend ls -la /app/media
```

4. **Resource Usage Issues**

```bash
# Using Make (Recommended)
make production-check-resources

# Manual checks
docker stats
docker compose -f docker/production/docker-compose.yml top
```

### Volume Backups

```bash
# Using Make (Recommended)
make production-backup-volumes

# Manual backup process
docker run --rm \
    -v $(docker volume inspect -f '{{ .Mountpoint }}' personal-backend_postgres_data_prod):/source \
    -v $(pwd)/backups:/backup \
    alpine tar czf /backup/postgres_data_$(date +%Y%m%d).tar.gz -C /source .
```

## 📈 Performance Tuning

### Database Optimization

```bash
# Using Make (Recommended)
make production-db-status
make production-db-connections

# Manual monitoring
docker compose -f docker/production/docker-compose.yml exec db psql -U personal_production -c "\x" -c "SELECT * FROM pg_stat_activity;"
```
