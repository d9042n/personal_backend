# 🚀 Staging Environment Guide

Guide for deploying and testing in the staging environment.

## 📋 Overview

- Port: `8001` (http://localhost:8001)
- Purpose: Pre-production testing and QA
- Resources: 1.0 CPU, 1GB RAM
- Debug: Disabled
- Security: Similar to production

## 🚀 Deployment

1. **Setup Environment**

```bash
# Copy staging env file
cp .env.example .env.staging

# Edit configuration
nano .env.staging
```

2. **Configure Settings**

```env
DEBUG=False
SECRET_KEY=staging-secret-key
ALLOWED_HOSTS=staging.domain.com,localhost

# Database
DB_NAME=personal_staging
DB_USER=personal_staging
DB_PASSWORD=staging-password
DB_HOST=db
DB_PORT=5432

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
```

3. **Deploy Services**

```bash
# Build and start
make staging-build
make staging-up

# Initialize
make staging-migrate
make staging-collectstatic
```

## 📝 Common Tasks

### Service Management

```bash
# Check status
make staging-health

# View logs
make staging-logs

# Restart services
docker compose -f docker/staging/docker-compose.yml restart
```

### Database Operations

```bash
# Create backup
make staging-backup-volumes

# Check status
make staging-db-status
```

## 🔍 Testing Guide

### 1. API Testing

```bash
# Health check
curl http://localhost:8001/health/

# API endpoints
curl http://localhost:8001/api/v1/...
```

### 2. Performance Testing

```bash
# Monitor resources
make staging-check-resources

# Check DB connections
make staging-db-connections
```

### 3. Security Testing

- SSL/TLS configuration
- Authentication flows
- API rate limiting
- CORS settings

## ❗ Troubleshooting

### Service Issues

```bash
# Check service health
make staging-health

# View detailed logs
make staging-logs
```

### Database Issues

```bash
# Check DB status
make staging-db-status

# View DB logs
docker compose -f docker/staging/docker-compose.yml logs db
```

### Volume Issues

```bash
# Check permissions
make staging-check-volumes
```

## 📊 Monitoring

### Health Metrics

- Service status
- Response times
- Error rates
- Resource usage

### Database Metrics

- Connection count
- Query performance
- Cache hit rates

Need help? Contact the DevOps team.
