# 🐳 Docker Swarm Infrastructure Guide

A comprehensive guide for setting up and managing our Docker Swarm infrastructure for development, staging, and production environments.

## 📑 Table of Contents

- [Architecture Overview](#-architecture-overview)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Detailed Setup Guide](#-detailed-setup-guide)
- [Environment Management](#-environment-management)
- [Common Operations](#-common-operations)
- [Troubleshooting](#-troubleshooting)
- [Best Practices](#-best-practices)

## 🏗 Architecture Overview

### Development Environment

- Single-node setup
- Hot-reload enabled
- Direct volume mounts
- Local development optimized

### Staging/Production Environment

```
                           [Load Balancer]
                                 │
                    ┌────────────┴──────────────┐
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
- Access to a container registry

## 🚀 Quick Start

1. Initialize Swarm:

```bash
# On manager node
make swarm-init

# Copy join token and run on worker nodes
make swarm-join-token
```

2. Label nodes:

```bash
# Label database node
make node-label-db node=worker1

# Label cache node
make node-label-cache node=worker2
```

3. Deploy stack:

```bash
# Build and push images
make production-build
make production-push

# Deploy stack
make production-deploy
```

## 📖 Detailed Setup Guide

### 1. Environment Setup

#### Development

```bash
# Start development environment
make development-build
make development-up

# Access development environment
make development-shell
```

#### Staging

```bash
# Deploy staging environment
make staging-build
make staging-push
make staging-deploy

# Scale staging services
make staging-scale replicas=2
```

#### Production

```bash
# Deploy production environment
make production-build
make production-push
make production-deploy

# Scale production services
make production-scale replicas=3
```

### 2. Service Configuration

Each service is configured with specific resource limits and placement constraints:

#### Backend Service

```yaml
deploy:
  mode: replicated
  replicas: 3
  resources:
    limits:
      cpus: "0.75"
      memory: 1G
    reservations:
      cpus: "0.25"
      memory: 512M
  placement:
    constraints:
      - node.role==worker
```

#### Database Service

```yaml
deploy:
  mode: replicated
  replicas: 1
  placement:
    constraints:
      - node.labels.db==true
  resources:
    limits:
      cpus: "1.0"
      memory: 2G
```

## 🔄 Environment Management

### Development to Production Workflow

1. Develop locally:

```bash
make development-up
```

2. Test in staging:

```bash
make staging-build TAG=v1.0.0-rc1
make staging-push TAG=v1.0.0-rc1
make staging-deploy
```

3. Deploy to production:

```bash
make production-build TAG=v1.0.0
make production-push TAG=v1.0.0
make production-deploy
```

### Rolling Updates

```bash
# Update service with zero downtime
make production-update TAG=v1.0.1
```

## 🛠 Common Operations

### Monitoring

```bash
# Check service status
make production-ps

# View logs
make production-logs

# Inspect nodes
make swarm-nodes
```

### Scaling

```bash
# Scale backend service
make production-scale replicas=5

# Check scaling status
make production-services
```

### Database Operations

```bash
# Backup database
make db-backup

# Restore database
make db-restore file=backup_20240215_120000.sql
```

## 🚨 Troubleshooting

### Common Issues

1. Service Won't Start

```bash
# Check service logs
make production-logs

# Verify node resources
make swarm-inspect node=worker1
```

2. Node Communication Issues

```bash
# Verify network
make stack-networks

# Check node status
make swarm-nodes
```

## ✅ Best Practices

### 1. Resource Management

- Always set both limits and reservations
- Monitor resource usage
- Scale based on metrics

### 2. High Availability

- Use multiple manager nodes (3-5)
- Distribute workloads across nodes
- Implement proper backup strategies

### 3. Security

- Use overlay networks with encryption
- Implement secrets management
- Regular security audits

### 4. Monitoring

- Set up proper logging
- Implement health checks
- Monitor resource usage

## 📊 Resource Guidelines

### Recommended Configurations

| Service  | CPU Limit | Memory Limit | Replicas |
| -------- | --------- | ------------ | -------- |
| Backend  | 0.75      | 1GB          | 3-5      |
| Database | 1.0       | 2GB          | 1        |
| Redis    | 0.5       | 512MB        | 1        |

## 🔍 Additional Resources

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
