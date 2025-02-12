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

## 🔧 Environment Overview

### Development

- Django development server
- Hot reload enabled
- Debug mode ON
- Resource limits: 0.5 CPU, 512MB RAM per service
- Mounted volumes for live code changes

### Staging

- Gunicorn with 2 workers
- Debug mode OFF
- Resource limits: 1.0 CPU, 1GB RAM for backend
- Mimics production with reduced resources

### Production

- Gunicorn with 4 workers
- Debug mode OFF
- Resource limits: 2.0 CPU, 2GB RAM for backend
- Full security measures
- Regular backups

## 🚀 Quick Start

Choose the appropriate environment:

```bash
# Development
make development-build
make development-up

# Staging
make staging-build
make staging-up

# Production
make production-build
make production-up
```

## 📚 Documentation

Detailed setup instructions are available in each environment's README:

- [Development Guide](development/README.md)
- [Staging Guide](staging/README.md)
- [Production Guide](production/README.md)

## 🔐 Security Notes

- Never commit `.env` files
- Use different credentials for each environment
- Follow the principle of least privilege
- Keep Docker and dependencies updated

## 🤝 Contributing

Please read our [Contributing Guide](../CONTRIBUTING.md) for details on our code of conduct and development process.
