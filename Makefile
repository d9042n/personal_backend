# Environment variables
REGISTRY ?= localhost
TAG ?= latest

# Development environment
development-build:
	docker compose -f docker/development/docker-compose.yml build

development-up:
	docker compose -f docker/development/docker-compose.yml up

development-up-d:
	docker compose -f docker/development/docker-compose.yml up -d

development-down:
	docker compose -f docker/development/docker-compose.yml down

development-logs:
	docker compose -f docker/development/docker-compose.yml logs -f

development-shell:
	docker compose -f docker/development/docker-compose.yml run --rm backend python manage.py shell

development-migrate:
	docker compose -f docker/development/docker-compose.yml run --rm backend python manage.py migrate

development-makemigrations:
	docker compose -f docker/development/docker-compose.yml run --rm backend python manage.py makemigrations

development-createsuperuser:
	docker compose -f docker/development/docker-compose.yml run --rm backend python manage.py createsuperuser

# Swarm initialization and node management
swarm-init:
	docker swarm init

swarm-join-token:
	docker swarm join-token worker

node-label-db:
	docker node update --label-add db=true $(node)

node-label-cache:
	docker node update --label-add cache=true $(node)

# Staging environment
staging-build:
	docker build -t $(REGISTRY)/personal_backend:$(TAG)-staging -f docker/staging/Dockerfile .

staging-push:
	docker push $(REGISTRY)/personal_backend:$(TAG)-staging

staging-deploy:
	docker stack deploy -c docker/staging/docker-compose.yml personal-staging

staging-update:
	docker service update --image $(REGISTRY)/personal_backend:$(TAG)-staging personal-staging_backend

staging-scale:
	docker service scale personal-staging_backend=$(replicas)

staging-ps:
	docker stack ps personal-staging

staging-services:
	docker stack services personal-staging

staging-logs:
	docker service logs personal-staging_backend

staging-remove:
	docker stack rm personal-staging

# Production environment
production-build:
	docker build -t $(REGISTRY)/personal_backend:$(TAG) -f docker/production/Dockerfile .

production-push:
	docker push $(REGISTRY)/personal_backend:$(TAG)

production-deploy:
	docker stack deploy -c docker/production/docker-compose.yml personal

production-update:
	docker service update --image $(REGISTRY)/personal_backend:$(TAG) personal_backend

production-scale:
	docker service scale personal_backend=$(replicas)

production-ps:
	docker stack ps personal

production-services:
	docker stack services personal

production-logs:
	docker service logs personal_backend

production-remove:
	docker stack rm personal

# Monitoring and maintenance
swarm-nodes:
	docker node ls

swarm-inspect:
	docker node inspect $(node)

stack-services:
	docker service ls

stack-networks:
	docker network ls

# Database operations
db-backup:
	docker exec -t $$(docker ps -q -f name=personal_db) pg_dumpall -c -U postgres > backup_$$(date +%Y%m%d_%H%M%S).sql

db-restore:
	cat $(file) | docker exec -i $$(docker ps -q -f name=personal_db) psql -U postgres

# Cleanup
clean:
	docker system prune -f
	docker volume prune -f

# Help
help:
	@echo "🐳 Docker Swarm Management Commands"
	@echo ""
	@echo "Swarm Management:"
	@echo "  swarm-init              - Initialize Docker Swarm"
	@echo "  swarm-join-token        - Get worker join token"
	@echo "  swarm-nodes             - List all nodes"
	@echo "  node-label-db           - Label node for database (node=<NODE>)"
	@echo "  node-label-cache        - Label node for cache (node=<NODE>)"
	@echo ""
	@echo "Development:"
	@echo "  development-build       - Build development environment"
	@echo "  development-up          - Start development environment"
	@echo "  development-down        - Stop development environment"
	@echo "  development-logs        - View development logs"
	@echo ""
	@echo "Staging:"
	@echo "  staging-build          - Build staging image"
	@echo "  staging-push           - Push staging image to registry"
	@echo "  staging-deploy         - Deploy staging stack"
	@echo "  staging-update         - Update staging service"
	@echo "  staging-scale          - Scale staging service (replicas=<NUM>)"
	@echo "  staging-logs           - View staging logs"
	@echo ""
	@echo "Production:"
	@echo "  production-build       - Build production image"
	@echo "  production-push        - Push production image to registry"
	@echo "  production-deploy      - Deploy production stack"
	@echo "  production-update      - Update production service"
	@echo "  production-scale       - Scale production service (replicas=<NUM>)"
	@echo "  production-logs        - View production logs"
	@echo ""
	@echo "Maintenance:"
	@echo "  db-backup             - Backup database"
	@echo "  db-restore            - Restore database (file=<PATH>)"
	@echo "  clean                 - Clean unused Docker resources"

.PHONY: development-build development-up development-down development-logs development-shell \
	staging-build staging-push staging-deploy staging-update staging-scale staging-logs staging-remove \
	production-build production-push production-deploy production-update production-scale production-logs production-remove \
	swarm-init swarm-join-token node-label-db node-label-cache swarm-nodes swarm-inspect \
	stack-services stack-networks db-backup db-restore clean help
