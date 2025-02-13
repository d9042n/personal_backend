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
	docker compose -f docker/development/docker-compose.yml run --rm web python manage.py shell

development-migrate:
	docker compose -f docker/development/docker-compose.yml run --rm web python manage.py migrate

development-makemigrations:
	docker compose -f docker/development/docker-compose.yml run --rm web python manage.py makemigrations

development-createsuperuser:
	docker compose -f docker/development/docker-compose.yml run --rm web python manage.py createsuperuser

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
	docker compose -f docker/staging/docker-compose.yml run --rm web python manage.py migrate

staging-collectstatic:
	docker compose -f docker/staging/docker-compose.yml run --rm web python manage.py collectstatic --no-input

staging-health:
	docker compose -f docker/staging/docker-compose.yml ps
	@echo "\nChecking health endpoints..."
	@curl -s http://localhost:8000/health/
	@echo "\nChecking database..."
	@docker compose -f docker/staging/docker-compose.yml exec db pg_isready -U personal_staging

staging-check-volumes:
	@echo "Checking volume permissions..."
	docker compose -f docker/staging/docker-compose.yml exec backend ls -la /app/staticfiles
	docker compose -f docker/staging/docker-compose.yml exec backend ls -la /app/media
	docker compose -f docker/staging/docker-compose.yml exec db ls -la /var/lib/postgresql/data

staging-check-resources:
	docker stats --no-stream

staging-db-status:
	docker compose -f docker/staging/docker-compose.yml exec db psql -U personal_staging -c "SELECT count(*) FROM pg_stat_activity;"

staging-db-connections:
	docker compose -f docker/staging/docker-compose.yml exec db psql -U personal_staging -c "\x" -c "SELECT * FROM pg_stat_activity;"

staging-backup-volumes:
	@echo "Creating backup directory..."
	@mkdir -p backups/staging
	@echo "Backing up PostgreSQL data..."
	@docker run --rm \
		-v $$(docker volume inspect -f '{{ .Mountpoint }}' personal-backend_postgres_data_staging):/source \
		-v $$(pwd)/backups/staging:/backup \
		alpine tar czf /backup/postgres_data_$$(date +%Y%m%d).tar.gz -C /source .
	@echo "Backing up Redis data..."
	@docker run --rm \
		-v $$(docker volume inspect -f '{{ .Mountpoint }}' personal-backend_redis_data_staging):/source \
		-v $$(pwd)/backups/staging:/backup \
		alpine tar czf /backup/redis_data_$$(date +%Y%m%d).tar.gz -C /source .

# Production environment
production-build:
	docker compose -f docker/production/docker-compose.yml build

production-up:
	docker compose -f docker/production/docker-compose.yml up -d

production-down:
	docker compose -f docker/production/docker-compose.yml down

production-restart:
	docker compose -f docker/production/docker-compose.yml restart

production-ps:
	docker compose -f docker/production/docker-compose.yml ps

production-logs:
	docker compose -f docker/production/docker-compose.yml logs -f

production-logs-backend:
	docker compose -f docker/production/docker-compose.yml logs -f backend

production-logs-db:
	docker compose -f docker/production/docker-compose.yml logs -f db

production-logs-redis:
	docker compose -f docker/production/docker-compose.yml logs -f redis

production-migrate:
	docker compose -f docker/production/docker-compose.yml exec backend python manage.py migrate

production-collectstatic:
	docker compose -f docker/production/docker-compose.yml exec backend python manage.py collectstatic --noinput

# Testing
test:
	docker compose -f docker/development/docker-compose.yml run --rm web python manage.py test

test-coverage:
	docker compose -f docker/development/docker-compose.yml run --rm web coverage run manage.py test
	docker compose -f docker/development/docker-compose.yml run --rm web coverage report

# Database
db-backup:
	docker compose -f docker/production/docker-compose.yml exec db pg_dump -U personal_production personal_production > backup_$(shell date +%Y%m%d_%H%M%S).sql

db-restore:
	@if [ -z "$(file)" ]; then \
		echo "Please specify backup file: make db-restore file=backup_file.sql"; \
		exit 1; \
	fi
	docker compose -f docker/production/docker-compose.yml exec -T db psql -U personal_production personal_production < $(file)

# Cleanup
clean:
	docker system prune -f
	docker volume prune -f

# Production monitoring
production-health:
	docker compose -f docker/production/docker-compose.yml ps
	@echo "\nChecking health endpoints..."
	@curl -s http://localhost:8000/health/
	@echo "\nChecking database..."
	@docker compose -f docker/production/docker-compose.yml exec db pg_isready -U personal_production

production-check-volumes:
	@echo "Checking volume permissions..."
	docker compose -f docker/production/docker-compose.yml exec backend ls -la /app/staticfiles
	docker compose -f docker/production/docker-compose.yml exec backend ls -la /app/media
	@echo "Checking host volume permissions..."
	ls -la /var/www/personal/static
	ls -la /var/www/personal/media

production-check-resources:
	docker stats --no-stream

# Database maintenance
production-db-status:
	docker compose -f docker/production/docker-compose.yml exec db psql -U personal_production -c "SELECT count(*) FROM pg_stat_activity;"

production-db-connections:
	docker compose -f docker/production/docker-compose.yml exec db psql -U personal_production -c "\x" -c "SELECT * FROM pg_stat_activity;"

# Volume backups
production-backup-volumes:
	@echo "Creating backup directory..."
	@mkdir -p backups
	@echo "Backing up PostgreSQL data..."
	@docker run --rm \
		-v $$(docker volume inspect -f '{{ .Mountpoint }}' personal-backend_postgres_data_prod):/source \
		-v $$(pwd)/backups:/backup \
		alpine tar czf /backup/postgres_data_$$(date +%Y%m%d).tar.gz -C /source .
	@echo "Backing up Redis data..."
	@docker run --rm \
		-v $$(docker volume inspect -f '{{ .Mountpoint }}' personal-backend_redis_data_prod):/source \
		-v $$(pwd)/backups:/backup \
		alpine tar czf /backup/redis_data_$$(date +%Y%m%d).tar.gz -C /source .

# Development monitoring
development-health:
	docker compose -f docker/development/docker-compose.yml ps
	@echo "\nChecking health endpoints..."
	@curl -s http://localhost:8000/health/
	@echo "\nChecking database..."
	@docker compose -f docker/development/docker-compose.yml exec db pg_isready -U personal

development-check-volumes:
	@echo "Checking volume permissions..."
	docker compose -f docker/development/docker-compose.yml exec backend ls -la /app
	docker compose -f docker/development/docker-compose.yml exec db ls -la /var/lib/postgresql/data

development-check-resources:
	docker stats --no-stream

development-db-status:
	docker compose -f docker/development/docker-compose.yml exec db psql -U personal -c "SELECT count(*) FROM pg_stat_activity;"

development-db-connections:
	docker compose -f docker/development/docker-compose.yml exec db psql -U personal -c "\x" -c "SELECT * FROM pg_stat_activity;"

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
	@echo "  development-health          - Check health of development services"
	@echo "  development-check-volumes   - Check volume permissions"
	@echo "  development-check-resources - Monitor resource usage"
	@echo "  development-db-status       - Check database status"
	@echo "  development-db-connections  - View active database connections"
	@echo ""
	@echo "Staging:"
	@echo "  staging-build        - Build staging environment"
	@echo "  staging-up          - Start staging environment"
	@echo "  staging-down        - Stop staging environment"
	@echo "  staging-logs        - View staging logs"
	@echo "  staging-migrate     - Run migrations"
	@echo "  staging-health      - Check health of staging environment"
	@echo "  staging-check-volumes - Check volume permissions"
	@echo "  staging-check-resources - Monitor resource usage"
	@echo "  staging-db-status   - Check database status"
	@echo "  staging-db-connections - View active database connections"
	@echo "  staging-backup-volumes - Backup all data volumes"
	@echo ""
	@echo "Production:"
	@echo "  production-build          - Build production environment"
	@echo "  production-up            - Start production environment"
	@echo "  production-down          - Stop production environment"
	@echo "  production-restart        - Restart production environment"
	@echo "  production-ps             - List production containers"
	@echo "  production-logs           - View production logs"
	@echo "  production-logs-backend   - View backend logs"
	@echo "  production-logs-db        - View database logs"
	@echo "  production-logs-redis     - View Redis logs"
	@echo "  production-migrate        - Run migrations"
	@echo "  production-collectstatic  - Collect static files"
	@echo ""
	@echo "Testing:"
	@echo "  test               - Run tests"
	@echo "  test-coverage      - Run tests with coverage report"
	@echo ""
	@echo "Database:"
	@echo "  db-backup          - Backup database"
	@echo "  db-restore file=   - Restore database from file"
	@echo ""
	@echo "Monitoring:"
	@echo "  production-health          - Check health of all services"
	@echo "  production-check-volumes   - Check volume permissions"
	@echo "  production-check-resources - Monitor resource usage"
	@echo "  production-db-status       - Check database status"
	@echo "  production-db-connections  - View active database connections"
	@echo "  production-backup-volumes  - Backup all data volumes"
	@echo ""
	@echo "Cleanup:"
	@echo "  clean              - Remove unused Docker resources"

.PHONY: development-build development-up development-up-d development-down development-logs development-shell development-migrate development-makemigrations development-createsuperuser \
	staging-build staging-up staging-down staging-logs staging-migrate staging-collectstatic staging-health staging-check-volumes staging-check-resources staging-db-status staging-db-connections staging-backup-volumes \
	production-build production-up production-down production-restart production-ps production-logs production-logs-backend production-logs-db production-logs-redis production-migrate production-collectstatic \
	test test-coverage db-backup db-restore clean \
	production-health production-check-volumes production-check-resources \
	production-db-status production-db-connections production-backup-volumes \
	development-health development-check-volumes development-check-resources \
	development-db-status development-db-connections
