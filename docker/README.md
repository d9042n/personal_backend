# 🐳 Docker Swarm Deployment Guide

A comprehensive guide for deploying our application using Docker Swarm in both single-node and multi-node environments.

## 📑 Table of Contents

- [Architecture Overview](#-architecture-overview)
- [Prerequisites](#-prerequisites)
- [Single-Node Deployment](#-single-node-deployment)
- [Multi-Node Deployment](#-multi-node-deployment)
- [Common Operations](#-common-operations)
- [Monitoring & Maintenance](#-monitoring--maintenance)
- [Troubleshooting](#-troubleshooting)

## 🏗 Architecture Overview

### Single-Node Setup

```
                    [Docker Swarm Node]
                           │
         ┌─────────┬───────┴───────┬─────────┐
    [Backend x2] [Redis x1]    [Postgres x1]
```

### Multi-Node Setup

```
                        [Load Balancer]
                              │
                ┌─────────────┴─────────────┐
                │                           │
          [Manager Node]               [Manager Node]
                │                           │
     ┌─────┬────┴────┬─────┐       ┌─────┬──┴──┬─────┐
[Worker 1] [Worker 2] [Worker 3]  [DB]  [Redis] [Worker 4]
```

## 📋 Prerequisites

- Docker Engine 24.0+
- Docker Compose v2.0+
- Make utility
- Git
- Container Registry (optional for single node)

## 🚀 Single-Node Deployment

### 1. Initial Setup

```bash
# Clone repository
git clone <repository-url>
cd <project-directory>

# Initialize swarm
docker swarm init
```

### 2. Environment Configuration

```bash
# Create staging environment file
cat > .env.staging << EOF
POSTGRES_DB=personal_staging
POSTGRES_USER=personal_staging
POSTGRES_PASSWORD=<your-secure-password>
REDIS_HOST=redis
DATABASE_URL=postgresql://personal_staging:<your-secure-password>@db:5432/personal_staging
EOF

# Create production environment file
cat > .env.production << EOF
POSTGRES_DB=personal_production
POSTGRES_USER=personal_production
POSTGRES_PASSWORD=<your-secure-password>
REDIS_HOST=redis
DATABASE_URL=postgresql://personal_production:<your-secure-password>@db:5432/personal_production
EOF
```

### 3. Deploy Staging

```bash
# Build and deploy staging
make staging-build
make staging-deploy

# Verify deployment
make staging-ps
make staging-logs

# Run migrations
docker exec -it $(docker ps -q -f name=personal-staging_backend) python manage.py migrate
```

### 4. Deploy Production

```bash
# Build and deploy production
make production-build
make production-deploy

# Verify deployment
make production-ps
make production-logs

# Run migrations
docker exec -it $(docker ps -q -f name=personal_backend) python manage.py migrate
```

## 🌐 Multi-Node Deployment

### 1. Infrastructure Setup

```bash
# On first manager node
docker swarm init --advertise-addr <MANAGER1-IP>

# On second manager node (using token from first manager)
docker swarm join --token <MANAGER-TOKEN> <MANAGER1-IP>:2377

# On worker nodes (using worker token)
docker swarm join --token <WORKER-TOKEN> <MANAGER1-IP>:2377
```

### 2. Node Labeling

```bash
# Label database node
make node-label-db node=worker1

# Label cache node
make node-label-cache node=worker2
```

### 3. Registry Setup

```bash
# Log in to registry
docker login <your-registry>

# Build and push images
make production-build TAG=1.0.0
make production-push TAG=1.0.0
```

### 4. Deployment

```bash
# Deploy stack
make production-deploy

# Scale services
make production-scale replicas=3

# Verify deployment
make production-ps
make production-services
```

## 🛠 Common Operations

### Scaling Services

```bash
# Scale backend service
make production-scale replicas=3

# Check scaling status
make production-services
```

### Updates and Rollbacks

```bash
# Update service
make production-update TAG=1.0.1

# Monitor update
make production-ps
make production-logs

# Rollback if needed
make production-update TAG=1.0.0
```

### Database Operations

```bash
# Backup database
make db-backup

# Restore database
make db-restore file=backup_20240215_120000.sql
```

## 📊 Resource Allocation

### Single-Node Configuration

| Service  | CPU Limit | Memory Limit | Replicas |
| -------- | --------- | ------------ | -------- |
| Backend  | 0.75      | 1GB          | 2        |
| Database | 0.50      | 1GB          | 1        |
| Redis    | 0.25      | 512MB        | 1        |

### Multi-Node Configuration

| Service  | CPU Limit | Memory Limit | Replicas |
| -------- | --------- | ------------ | -------- |
| Backend  | 0.75      | 1GB          | 3-5      |
| Database | 1.0       | 2GB          | 1        |
| Redis    | 0.50      | 512MB        | 1        |

## 🔍 Health Monitoring

### Service Health Checks

```bash
# Check service status
make production-ps

# View service logs
make production-logs

# Monitor resources
docker stats
```

### Automated Health Checks

All services include built-in health checks:

- Backend: HTTP check on /health/
- Database: pg_isready check
- Redis: ping check

## 🚨 Troubleshooting

### Common Issues

1. **Service Won't Start**

```bash
# Check service logs
make production-logs

# Verify resources
docker stats
```

2. **Database Connection Issues**

```bash
# Check database logs
docker service logs personal_db

# Verify network connectivity
docker network inspect backend
```

3. **Memory/CPU Issues**

```bash
# Check resource usage
docker stats

# Scale down if needed
make production-scale replicas=2
```

## 📝 Best Practices

### Security

- Use secrets for sensitive data
- Enable network encryption
- Regular security updates
- Proper user permissions

### Backups

- Regular database backups
- Configuration backups
- Documented restore procedures

### Monitoring

- Resource monitoring
- Log aggregation
- Health check alerts
- Performance metrics

### Updates

- Rolling updates
- Version control
- Backup before updates
- Test in staging first

## 🔄 Lifecycle Management

### Development Workflow

1. Develop locally
2. Test in staging
3. Deploy to production
4. Monitor and maintain

### Update Process

1. Build new version
2. Test in staging
3. Rolling update in production
4. Monitor deployment

## 📚 Additional Resources

- [Docker Swarm Documentation](https://docs.docker.com/engine/swarm/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Docker Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

## 🤝 Contributing

Please read our [Contributing Guide](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🗂️ Directory Structure

```
docker/
├── development/
│   ├── Dockerfile
│   └── docker-compose.yml
├── production/
│   ├── Dockerfile
│   └── docker-compose.yml
├── staging/
│   ├── Dockerfile
│   └── docker-compose.yml
└── README.md
```

## 🛠️ Common Tasks

### Initial Setup

1. Initialize Swarm cluster
2. Label nodes appropriately
3. Create overlay networks
4. Configure secrets

### Deployment

1. Build images
2. Push to registry
3. Deploy stack
4. Verify services

### Maintenance

1. Monitor resources
2. Rotate logs
3. Backup data
4. Update services

## 🚨 Troubleshooting

1. **Service Won't Start**

   - Check logs: `docker service logs <service>`
   - Verify resources: `docker node inspect <node>`
   - Check network: `docker network inspect <network>`

2. **Performance Issues**
   - Monitor resources: `docker stats`
   - Check load balancing
   - Verify network latency

## 📝 Commands Reference

```bash
# Swarm Management
docker swarm init
docker node ls
docker node promote/demote

# Stack Management
docker stack deploy -c docker-compose.yml myapp
docker stack services myapp
docker stack ps myapp

# Service Management
docker service ls
docker service scale myapp_backend=5
docker service update --image newimage:tag myapp_backend
```

## Best Practices

1. **Environment Separation**

   - Different Dockerfile and docker-compose.yml for each environment
   - Environment-specific configurations via .env files

2. **Security**

   - Non-root user in containers
   - Internal networks for service communication
   - Proper permission settings

3. **Resource Management**

   - Memory limits configured
   - CPU allocation defined
   - Proper logging rotation

4. **Health Checks**

   - All services have health checks
   - Proper dependency management
   - Reasonable retry policies

5. **Scaling**
   - Services can be scaled horizontally
   - Load balancing configured
   - Resource limits per container

## Directory Structure
