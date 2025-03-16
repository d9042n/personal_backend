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

# Monitoring - Development environment
monitoring-development-up:
	docker compose -f docker/monitoring/development/docker-compose.yml up -d
	@echo "Monitoring stack started in development environment."
	@echo "Grafana: http://localhost:3000 (admin/admin)"
	@echo "Prometheus: http://localhost:9090"
	@echo "Loki: http://localhost:3100"

monitoring-development-down:
	docker compose -f docker/monitoring/development/docker-compose.yml down
	@echo "Monitoring stack stopped in development environment."

monitoring-development-restart:
	docker compose -f docker/monitoring/development/docker-compose.yml restart
	@echo "Monitoring stack restarted in development environment."

monitoring-development-logs:
	docker compose -f docker/monitoring/development/docker-compose.yml logs -f

monitoring-development-status:
	docker compose -f docker/monitoring/development/docker-compose.yml ps

# Combined Development targets
development-all-up:
	docker compose -f docker/development/docker-compose.yml up -d
	docker compose -f docker/monitoring/development/docker-compose.yml up -d
	@echo "App and monitoring stack started in development environment."
	@echo "Grafana: http://localhost:3000 (admin/admin)"
	@echo "Prometheus: http://localhost:9090"
	@echo "Loki: http://localhost:3100"

development-all-down:
	docker compose -f docker/development/docker-compose.yml down
	docker compose -f docker/monitoring/development/docker-compose.yml down
	@echo "App and monitoring stack stopped in development environment."

# Staging environment
staging-build:
	docker compose -f docker/staging/docker-compose.yml build

staging-up:
	docker compose -f docker/staging/docker-compose.yml up -d

staging-down:
	docker compose -f docker/staging/docker-compose.yml down

staging-logs:
	docker compose -f docker/staging/docker-compose.yml logs -f

staging-migrate:
	docker compose -f docker/staging/docker-compose.yml run --rm backend python manage.py migrate

staging-collectstatic:
	docker compose -f docker/staging/docker-compose.yml run --rm backend python manage.py collectstatic --no-input

# Monitoring - Staging environment
monitoring-staging-up:
	docker compose -f docker/monitoring/staging/docker-compose.yml up -d
	@echo "Monitoring stack started in staging environment."
	@echo "Grafana: http://localhost:3000 (admin/StrongStaginPassword123!)"
	@echo "Prometheus: http://localhost:9090"
	@echo "Loki: http://localhost:3100"

monitoring-staging-down:
	docker compose -f docker/monitoring/staging/docker-compose.yml down
	@echo "Monitoring stack stopped in staging environment."

monitoring-staging-restart:
	docker compose -f docker/monitoring/staging/docker-compose.yml restart
	@echo "Monitoring stack restarted in staging environment."

monitoring-staging-logs:
	docker compose -f docker/monitoring/staging/docker-compose.yml logs -f

monitoring-staging-status:
	docker compose -f docker/monitoring/staging/docker-compose.yml ps

# Combined Staging targets
staging-all-up:
	docker compose -f docker/staging/docker-compose.yml up -d
	docker compose -f docker/monitoring/staging/docker-compose.yml up -d
	@echo "App and monitoring stack started in staging environment."
	@echo "Grafana: http://localhost:3000 (admin/StrongStaginPassword123!)"
	@echo "Prometheus: http://localhost:9090"
	@echo "Loki: http://localhost:3100"

staging-all-down:
	docker compose -f docker/staging/docker-compose.yml down
	docker compose -f docker/monitoring/staging/docker-compose.yml down
	@echo "App and monitoring stack stopped in staging environment."

# Production environment
production-build:
	docker compose -f docker/production/docker-compose.yml build

production-up:
	docker compose -f docker/production/docker-compose.yml up -d

production-down:
	docker compose -f docker/production/docker-compose.yml down

production-logs:
	docker compose -f docker/production/docker-compose.yml logs -f

production-migrate:
	docker compose -f docker/production/docker-compose.yml run --rm backend python manage.py migrate

production-collectstatic:
	docker compose -f docker/production/docker-compose.yml run --rm backend python manage.py collectstatic --no-input

# Monitoring - Production environment
monitoring-production-up:
	docker compose -f docker/monitoring/production/docker-compose.yml up -d
	@echo "Monitoring stack started in production environment."
	@echo "Grafana: http://localhost:3000 (admin/set via GRAFANA_ADMIN_PASSWORD)"
	@echo "Prometheus: http://localhost:9090"
	@echo "Loki: http://localhost:3100"

monitoring-production-down:
	docker compose -f docker/monitoring/production/docker-compose.yml down
	@echo "Monitoring stack stopped in production environment."

monitoring-production-restart:
	docker compose -f docker/monitoring/production/docker-compose.yml restart
	@echo "Monitoring stack restarted in production environment."

monitoring-production-logs:
	docker compose -f docker/monitoring/production/docker-compose.yml logs -f

monitoring-production-status:
	docker compose -f docker/monitoring/production/docker-compose.yml ps

# Combined Production targets
production-all-up:
	docker compose -f docker/production/docker-compose.yml up -d
	docker compose -f docker/monitoring/production/docker-compose.yml up -d
	@echo "App and monitoring stack started in production environment."
	@echo "Grafana: http://localhost:3000 (admin/set via GRAFANA_ADMIN_PASSWORD)"
	@echo "Prometheus: http://localhost:9090"
	@echo "Loki: http://localhost:3100"

production-all-down:
	docker compose -f docker/production/docker-compose.yml down
	docker compose -f docker/monitoring/production/docker-compose.yml down
	@echo "App and monitoring stack stopped in production environment."

# Testing
test:
	docker compose -f docker/development/docker-compose.yml run --rm backend python manage.py test

test-coverage:
	docker compose -f docker/development/docker-compose.yml run --rm backend coverage run manage.py test
	docker compose -f docker/development/docker-compose.yml run --rm backend coverage report

# Database
db-backup:
	docker compose -f docker/production/docker-compose.yml exec db pg_dump -U personal_production personal_production > backup_$(shell date +%Y%m%d_%H%M%S).sql

db-restore:
	docker compose -f docker/production/docker-compose.yml exec -T db psql -U personal_production personal_production < $(file)

# Cleanup
clean:
	docker system prune -f
	docker volume prune -f

clean-all:
	@echo "⚠️  WARNING: This will remove ALL Docker containers, images, volumes, and networks ⚠️"
	@echo "Are you sure you want to continue? [y/N] " && read ans && [ $${ans:-N} = y ]
	@echo "🧹 Stopping all containers..."
	@docker stop $$(docker ps -aq) 2>/dev/null || true
	@echo "🧹 Removing all containers..."
	@docker rm $$(docker ps -aq) 2>/dev/null || true
	@echo "🧹 Removing all images..."
	@docker rmi $$(docker images -q) --force 2>/dev/null || true
	@echo "🧹 Removing all volumes..."
	@docker volume rm $$(docker volume ls -q) 2>/dev/null || true
	@echo "🧹 Removing all networks..."
	@docker network rm $$(docker network ls -q) 2>/dev/null || true
	@echo "✅ All Docker resources have been removed!"

# Help
help:
	@echo "Available commands:"
	@echo "Development:"
	@echo "  development-build             - Build development environment"
	@echo "  development-up                - Start development environment"
	@echo "  development-up-d              - Start development environment in detached mode"
	@echo "  development-down              - Stop development environment"
	@echo "  development-logs              - View development logs"
	@echo "  development-shell             - Open Django shell"
	@echo "  development-migrate           - Run migrations"
	@echo "  development-makemigrations    - Create new migrations"
	@echo "  development-createsuperuser   - Create superuser"
	@echo "  development-all-up            - Start both app and monitoring in development"
	@echo "  development-all-down          - Stop both app and monitoring in development"
	@echo ""
	@echo "Staging:"
	@echo "  staging-build                 - Build staging environment"
	@echo "  staging-up                    - Start staging environment"
	@echo "  staging-down                  - Stop staging environment"
	@echo "  staging-logs                  - View staging logs"
	@echo "  staging-migrate               - Run migrations"
	@echo "  staging-collectstatic         - Collect static files"
	@echo "  staging-all-up                - Start both app and monitoring in staging"
	@echo "  staging-all-down              - Stop both app and monitoring in staging"
	@echo ""
	@echo "Production:"
	@echo "  production-build              - Build production environment"
	@echo "  production-up                 - Start production environment"
	@echo "  production-down               - Stop production environment"
	@echo "  production-logs               - View production logs"
	@echo "  production-migrate            - Run migrations"
	@echo "  production-collectstatic      - Collect static files"
	@echo "  production-all-up             - Start both app and monitoring in production"
	@echo "  production-all-down           - Stop both app and monitoring in production"
	@echo ""
	@echo "Monitoring:"
	@echo "  Development:"
	@echo "    monitoring-development-up           - Start monitoring stack in development"
	@echo "    monitoring-development-down         - Stop monitoring stack in development"
	@echo "    monitoring-development-restart      - Restart monitoring stack in development"
	@echo "    monitoring-development-logs         - View monitoring logs in development"
	@echo "    monitoring-development-status       - Check monitoring status in development"
	@echo ""
	@echo "  Staging:"
	@echo "    monitoring-staging-up               - Start monitoring stack in staging"
	@echo "    monitoring-staging-down             - Stop monitoring stack in staging"
	@echo "    monitoring-staging-restart          - Restart monitoring stack in staging"
	@echo "    monitoring-staging-logs             - View monitoring logs in staging"
	@echo "    monitoring-staging-status           - Check monitoring status in staging"
	@echo ""
	@echo "  Production:"
	@echo "    monitoring-production-up            - Start monitoring stack in production"
	@echo "    monitoring-production-down          - Stop monitoring stack in production"
	@echo "    monitoring-production-restart       - Restart monitoring stack in production"
	@echo "    monitoring-production-logs          - View monitoring logs in production"
	@echo "    monitoring-production-status        - Check monitoring status in production"
	@echo ""
	@echo "Testing:"
	@echo "  test                        - Run tests"
	@echo "  test-coverage               - Run tests with coverage report"
	@echo ""
	@echo "Database:"
	@echo "  db-backup                   - Backup production database"
	@echo "  db-restore file=<filename>  - Restore database from backup"
	@echo ""
	@echo "Cleanup:"
	@echo "  clean                       - Clean unused Docker resources (dangling images, stopped containers)"
	@echo "  clean-all                   - Remove ALL Docker containers, images, volumes, and networks (use with caution!)"

.PHONY: development-build development-up development-up-d development-down development-logs development-shell development-migrate development-makemigrations development-createsuperuser \
	staging-build staging-up staging-down staging-logs staging-migrate staging-collectstatic \
	production-build production-up production-down production-logs production-migrate production-collectstatic \
	test test-coverage db-backup db-restore clean clean-all help \
	monitoring-development-up monitoring-development-down monitoring-development-restart monitoring-development-logs monitoring-development-status \
	monitoring-staging-up monitoring-staging-down monitoring-staging-restart monitoring-staging-logs monitoring-staging-status \
	monitoring-production-up monitoring-production-down monitoring-production-restart monitoring-production-logs monitoring-production-status \
	development-all-up development-all-down staging-all-up staging-all-down production-all-up production-all-down
