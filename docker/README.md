# 🐳 Docker Configuration Guide

This directory contains Docker configurations for different environments of the Personal Backend project.

## 📋 Directory Structure

```
docker/
├── development/         # Development environment
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── README.md
├── staging/            # Staging environment
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── README.md
├── production/         # Production environment
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── README.md
└── README.md          # This file
```

## 📋 Environment Overview

### Development (Local)

- Port: `8002` (Backend), `5432` (DB), `6379` (Redis)
- Purpose: Local development with hot reload
- Features:
  - Django development server
  - Direct database access
  - Debug mode ON
  - Volume mounts for live code changes
  - Resource limits: 0.5 CPU, 512MB RAM per service

### Staging

- Port: `8001` (Backend only)
- Purpose: Testing before production
- Features:
  - Gunicorn with 2 workers
  - Debug mode OFF
  - Resource limits: 1.0 CPU, 1GB RAM for backend
  - Mimics production with reduced resources

### Production

- Port: `8000` (Backend only)
- Purpose: Live deployment
- Features:
  - Gunicorn with 4 workers
  - Debug mode OFF
  - Resource limits: 2.0 CPU, 2GB RAM for backend
  - Full security measures
  - Regular backups

## 🚀 Quick Start

Choose the appropriate environment:

```bash
# Development (Local)
make development-build
make development-up
# Access at http://localhost:8002

# Staging
make staging-build
make staging-up
# Access at http://localhost:8001

# Production
make production-build
make production-up
# Access at http://localhost:8000
```

## 🔐 Security Notes

1. **Port Exposure**

   - Development: All ports exposed for local development
   - Staging: Only backend port exposed
   - Production: Only backend port exposed (should be behind reverse proxy)

2. **Environment Variables**

   - Use different .env files for each environment
   - Never commit .env files
   - Use strong passwords in staging/production

3. **Network Security**
   - Development: Local access only
   - Staging: Limited access, basic auth recommended
   - Production: SSL/TLS required, proper authentication

## 📚 Documentation

Detailed setup instructions for each environment:

- [Development Guide](development/README.md) - Local development setup
- [Staging Guide](staging/README.md) - Pre-production testing
- [Production Guide](production/README.md) - Live deployment

Each environment has its own:

- Docker configuration
- Environment variables
- Resource limits
- Security settings
- Monitoring setup

## 🔧 Common Tasks

### Check Service Status

```bash
# Development
make development-health

# Staging
make staging-health

# Production
make production-health
```

### View Logs

```bash
# Development
make development-logs

# Staging
make staging-logs

# Production
make production-logs
```

### Database Operations

```bash
# Development (local access)
make development-db-status

# Staging
make staging-db-status

# Production
make production-db-status
```

## 🤝 Contributing

1. Use development environment for local work
2. Test changes in staging before production
3. Follow security guidelines for each environment
4. Keep documentation updated
