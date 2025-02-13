# 🐳 Local Development Guide

This guide explains how to run the Personal Backend project in a local development environment using Docker.

## 🚀 Quick Start

1. **Setup Project**

```bash
# Clone repository
git clone https://github.com/yourusername/personal-backend.git
cd personal-backend

# Copy environment file
cp .env.example .env.development
```

2. **Configure Environment**
   Edit `.env.development` with these required variables:

```env
DEBUG=True
SECRET_KEY=dev-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=personal
DB_USER=personal
DB_PASSWORD=devpassword
DB_HOST=db
DB_PORT=5432

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
```

3. **Start Development**

```bash
# Using Make (recommended)
make development-up-d

# Or using Docker Compose directly
docker compose -f docker/development/docker-compose.yml up -d
```

4. **Access Services**

- Backend API: http://localhost:8002
- Database: localhost:5434
- Redis: localhost:6381

## 🛠 Development Environment

### Container Services

| Service | Description                    | Port Mapping | Resource Limits      |
| ------- | ------------------------------ | ------------ | -------------------- |
| backend | Python 3.11 Django application | 8002 -> 8000 | CPU: 0.5, RAM: 512MB |
| db      | PostgreSQL 15                  | 5434 -> 5432 | CPU: 0.5, RAM: 512MB |
| redis   | Redis 7                        | 6381 -> 6379 | CPU: 0.5, RAM: 512MB |

### Volume Mounts

- Application code: `../../:/app:cached`
- Python packages: `python-packages:/usr/local/lib/python3.11/site-packages/`
- Postgres data: `postgres_data_dev:/var/lib/postgresql/data`
- Redis data: `redis_data_dev:/data`

## 📝 Common Commands

### Basic Operations

```bash
# Build services
make development-build
# or: docker compose -f docker/development/docker-compose.yml build

# Start services (attached)
make development-up
# or: docker compose -f docker/development/docker-compose.yml up

# Start services (detached)
make development-up-d
# or: docker compose -f docker/development/docker-compose.yml up -d

# Stop services
make development-down
# or: docker compose -f docker/development/docker-compose.yml down

# View logs
make development-logs
# or: docker compose -f docker/development/docker-compose.yml logs -f
```

### Development Commands

```bash
# Access Django shell
make development-shell
# or: docker compose -f docker/development/docker-compose.yml exec backend python manage.py shell

# Run migrations
make development-migrate
# or: docker compose -f docker/development/docker-compose.yml exec backend python manage.py migrate

# Create migrations
make development-makemigrations
# or: docker compose -f docker/development/docker-compose.yml exec backend python manage.py makemigrations

# Create superuser
make development-createsuperuser
# or: docker compose -f docker/development/docker-compose.yml exec backend python manage.py createsuperuser
```

### Monitoring Commands

```bash
# Check health status
make development-health
# or: docker compose -f docker/development/docker-compose.yml ps && curl -s http://localhost:8000/health/

# Check volume permissions
make development-check-volumes
# or: docker compose -f docker/development/docker-compose.yml exec backend ls -la /app

# Monitor resource usage
make development-check-resources
# or: docker stats --no-stream

# Check database status
make development-db-status
# or: docker compose -f docker/development/docker-compose.yml exec db psql -U personal -c "SELECT count(*) FROM pg_stat_activity;"
```

## 🔄 Development Features

### Auto-Reload

The development server automatically reloads when Python code changes are detected.

### Health Checks

- Backend: Checks `/health/` endpoint every 30s
- Database: Checks PostgreSQL readiness every 10s
- Redis: Checks connection every 10s

### Resource Management

All services have resource limits configured:

- CPU: 0.5 cores
- Memory: 512MB

## ❗ Troubleshooting

### Port Conflicts

If you see port binding errors, check if these ports are available:

- 8002 (Backend)
- 5434 (PostgreSQL)
- 6381 (Redis)

```bash
# Check ports on Linux/MacOS
sudo lsof -i :8002
sudo lsof -i :5434
sudo lsof -i :6381
```

### Database Reset

```bash
# Using Make
make development-down
docker volume rm development_postgres_data_dev
make development-up-d
make development-migrate

# Or using Docker Compose directly
docker compose -f docker/development/docker-compose.yml down
docker volume rm development_postgres_data_dev
docker compose -f docker/development/docker-compose.yml up -d
docker compose -f docker/development/docker-compose.yml exec backend python manage.py migrate
```

### Logs

```bash
# Using Make
make development-logs

# Or specific service logs using Docker Compose
docker compose -f docker/development/docker-compose.yml logs backend
docker compose -f docker/development/docker-compose.yml logs db
docker compose -f docker/development/docker-compose.yml logs redis
```

### Container Shell Access

```bash
# Backend container
make development-shell
# or: docker compose -f docker/development/docker-compose.yml exec backend bash

# Database container
docker compose -f docker/development/docker-compose.yml exec db psql -U personal
```

## 📚 Additional Notes

- All services are configured to restart automatically unless stopped manually
- Log rotation is enabled for database and redis (max 3 files of 10MB each)
- The backend container runs as a non-root user for security
- Python dependencies are built in a separate stage to keep the final image small

Need help? Check our [Contributing Guide](../../CONTRIBUTING.md) or reach out to the team!
