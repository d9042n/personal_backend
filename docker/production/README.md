# 🚀 Production Deployment Guide

Guide for deploying and maintaining the production environment.

## 📋 Overview

- Port: `8000` (Behind Nginx)
- Purpose: Live production environment
- Resources: 2.0 CPU, 2GB RAM
- Debug: Disabled
- Security: Maximum security measures

## 🚀 Initial Deployment

1. **Setup Environment**

```bash
# Copy production env file
cp .env.example .env.production

# Edit configuration
nano .env.production
```

2. **Configure Settings**

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
# Build and start
make production-build
make production-up

# Initialize
make production-migrate
make production-collectstatic
```

## 🔐 Security Checklist

- [ ] Strong passwords set
- [ ] SSL/TLS configured
- [ ] Firewall rules updated
- [ ] Nginx proxy configured
- [ ] Backups scheduled
- [ ] Monitoring enabled
- [ ] Rate limiting configured

## 📝 Maintenance

### Updates & Deployments

```bash
# Pull updates
git pull origin main

# Deploy changes
make production-build
make production-up
make production-migrate
```

### Backups

```bash
# Database backup
make db-backup

# Volume backup
make production-backup-volumes
```

## 📊 Monitoring

### Health Checks

```bash
# Service status
make production-health

# Resource usage
make production-check-resources
```

### Logs

```bash
# All services
make production-logs

# Specific services
make production-logs-backend
make production-logs-db
make production-logs-redis
```

## ❗ Emergency Procedures

### Service Recovery

```bash
# Quick restart
make production-restart

# Full restart
make production-down
make production-up
```

### Database Recovery

```bash
# Restore from backup
make db-restore file=backup_YYYYMMDD.sql
```

### Common Issues

1. **High Load**

```bash
# Check resources
make production-check-resources

# Monitor connections
make production-db-connections
```

2. **Service Failures**

```bash
# Check health
make production-health

# View errors
make production-logs
```

Need help? Contact the SRE team immediately.
