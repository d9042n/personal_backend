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

# Help
help:
	@echo "Available commands:"
	@echo "Development:"
	@echo "  development-build            - Build development environment"
	@echo "  development-up              - Start development environment"
	@echo "  development-up-d            - Start development environment in detached mode"
	@echo "  development-down            - Stop development environment"
	@echo "  development-logs            - View development logs"
	@echo "  development-shell           - Open Django shell"
	@echo "  development-migrate         - Run migrations"
	@echo "  development-makemigrations  - Create new migrations"
	@echo "  development-createsuperuser - Create superuser"
	@echo ""
	@echo "Staging:"
	@echo "  staging-build        - Build staging environment"
	@echo "  staging-up          - Start staging environment"
	@echo "  staging-down        - Stop staging environment"
	@echo "  staging-logs        - View staging logs"
	@echo "  staging-migrate     - Run migrations"
	@echo ""
	@echo "Production:"
	@echo "  production-build          - Build production environment"
	@echo "  production-up            - Start production environment"
	@echo "  production-down          - Stop production environment"
	@echo "  production-logs          - View production logs"
	@echo "  production-migrate       - Run migrations"
	@echo ""
	@echo "Testing:"
	@echo "  test               - Run tests"
	@echo "  test-coverage      - Run tests with coverage report"
	@echo ""
	@echo "Database:"
	@echo "  db-backup          - Backup database"
	@echo "  db-restore file=   - Restore database from file"
	@echo ""
	@echo "Cleanup:"
	@echo "  clean              - Remove unused Docker resources"

.PHONY: development-build development-up development-up-d development-down development-logs development-shell development-migrate development-makemigrations development-createsuperuser \
	staging-build staging-up staging-down staging-logs staging-migrate staging-collectstatic \
	production-build production-up production-down production-logs production-migrate production-collectstatic \
	test test-coverage db-backup db-restore clean help
