# Define colors
CYAN := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
BLUE := \033[34m
MAGENTA := \033[35m
BOLD := \033[1m
RESET := \033[0m

.PHONY: development-build development-up development-up-d development-down development-restart development-logs development-shell development-migrate development-makemigrations development-createsuperuser \
	staging-build staging-up staging-down staging-restart staging-logs staging-migrate staging-collectstatic \
	production-build production-up production-down production-restart production-logs production-migrate production-collectstatic \
	test test-coverage db-backup db-restore clean clean-all help \
	monitoring-development-up monitoring-development-down monitoring-development-restart monitoring-development-logs monitoring-development-status \
	monitoring-staging-up monitoring-staging-down monitoring-staging-restart monitoring-staging-logs monitoring-staging-status \
	monitoring-production-up monitoring-production-down monitoring-production-restart monitoring-production-logs monitoring-production-status \
	development-all-up development-all-down development-all-restart staging-all-up staging-all-down staging-all-restart production-all-up production-all-down production-all-restart

# Default target when no arguments are given to make
.DEFAULT_GOAL := help

# ======================================
# 🛠️  DEVELOPMENT ENVIRONMENT
# ======================================
development-build:
	@echo "$(BLUE)$(BOLD)🚀 Building development environment...$(RESET)"
	docker compose -f docker/development/docker-compose.yml --env-file .env.development build
	@echo "$(GREEN)✅ Development environment built successfully.$(RESET)"

development-up:
	@echo "$(BLUE)$(BOLD)🚀 Starting development environment...$(RESET)"
	docker compose -f docker/development/docker-compose.yml --env-file .env.development up
	@echo "$(GREEN)✅ Development environment started successfully.$(RESET)"

development-up-d:
	@echo "$(BLUE)$(BOLD)🚀 Starting development environment in detached mode...$(RESET)"
	docker compose -f docker/development/docker-compose.yml --env-file .env.development up -d
	@echo "$(GREEN)✅ Development environment started in detached mode.$(RESET)"

development-down:
	@echo "$(BLUE)$(BOLD)🛑 Stopping development environment...$(RESET)"
	docker compose -f docker/development/docker-compose.yml --env-file .env.development down
	@echo "$(GREEN)✅ Development environment stopped successfully.$(RESET)"

development-restart:
	@echo "$(BLUE)$(BOLD)🔄 Restarting development environment...$(RESET)"
	docker compose -f docker/development/docker-compose.yml --env-file .env.development restart
	@echo "$(GREEN)✅ Development environment restarted successfully.$(RESET)"

development-logs:
	@echo "$(BLUE)$(BOLD)📋 Viewing development logs...$(RESET)"
	docker compose -f docker/development/docker-compose.yml --env-file .env.development logs -f

development-shell:
	@echo "$(BLUE)$(BOLD)🔧 Opening Django shell in development environment...$(RESET)"
	docker compose -f docker/development/docker-compose.yml --env-file .env.development run --rm backend python manage.py shell

development-migrate:
	@echo "$(BLUE)$(BOLD)🔧 Running migrations in development environment...$(RESET)"
	docker compose -f docker/development/docker-compose.yml --env-file .env.development run --rm backend python manage.py migrate
	@echo "$(GREEN)✅ Migrations applied successfully.$(RESET)"

development-makemigrations:
	@echo "$(BLUE)$(BOLD)🔧 Creating migrations in development environment...$(RESET)"
	docker compose -f docker/development/docker-compose.yml --env-file .env.development run --rm backend python manage.py makemigrations
	@echo "$(GREEN)✅ Migrations created successfully.$(RESET)"

development-createsuperuser:
	@echo "$(BLUE)$(BOLD)👤 Creating superuser in development environment...$(RESET)"
	docker compose -f docker/development/docker-compose.yml --env-file .env.development run --rm backend python manage.py createsuperuser

# ======================================
# 📊 MONITORING - DEVELOPMENT
# ======================================
monitoring-development-up:
	@echo "$(MAGENTA)$(BOLD)📊 Starting monitoring stack in development environment...$(RESET)"
	docker compose -f docker/monitoring/development/docker-compose.yml --env-file .env.development up -d
	@echo "$(GREEN)✅ Monitoring stack started in development environment.$(RESET)"
	@echo "$(CYAN)ℹ️  Grafana: http://localhost:3000 (admin/admin)$(RESET)"
	@echo "$(CYAN)ℹ️  Prometheus: http://localhost:9090$(RESET)"
	@echo "$(CYAN)ℹ️  Loki: http://localhost:3100$(RESET)"

monitoring-development-down:
	@echo "$(MAGENTA)$(BOLD)🛑 Stopping monitoring stack in development environment...$(RESET)"
	docker compose -f docker/monitoring/development/docker-compose.yml --env-file .env.development down
	@echo "$(GREEN)✅ Monitoring stack stopped in development environment.$(RESET)"

monitoring-development-restart:
	@echo "$(MAGENTA)$(BOLD)🔄 Restarting monitoring stack in development environment...$(RESET)"
	docker compose -f docker/monitoring/development/docker-compose.yml --env-file .env.development restart
	@echo "$(GREEN)✅ Monitoring stack restarted in development environment.$(RESET)"

monitoring-development-logs:
	@echo "$(MAGENTA)$(BOLD)📋 Viewing monitoring logs in development environment...$(RESET)"
	docker compose -f docker/monitoring/development/docker-compose.yml --env-file .env.development logs -f

monitoring-development-status:
	@echo "$(MAGENTA)$(BOLD)📋 Checking monitoring status in development environment...$(RESET)"
	docker compose -f docker/monitoring/development/docker-compose.yml --env-file .env.development ps

# ======================================
# 🔄 COMBINED DEVELOPMENT TARGETS
# ======================================
development-all-up:
	@echo "$(CYAN)$(BOLD)🚀 Starting app and monitoring stack in development environment...$(RESET)"
	docker compose -f docker/development/docker-compose.yml --env-file .env.development up -d
	docker compose -f docker/monitoring/development/docker-compose.yml --env-file .env.development up -d
	@echo "$(GREEN)✅ App and monitoring stack started in development environment.$(RESET)"
	@echo "$(CYAN)ℹ️  Grafana: http://localhost:3000 (admin/admin)$(RESET)"
	@echo "$(CYAN)ℹ️  Prometheus: http://localhost:9090$(RESET)"
	@echo "$(CYAN)ℹ️  Loki: http://localhost:3100$(RESET)"

development-all-down:
	@echo "$(CYAN)$(BOLD)🛑 Stopping app and monitoring stack in development environment...$(RESET)"
	docker compose -f docker/development/docker-compose.yml --env-file .env.development down
	docker compose -f docker/monitoring/development/docker-compose.yml --env-file .env.development down
	@echo "$(GREEN)✅ App and monitoring stack stopped in development environment.$(RESET)"

development-all-restart:
	@echo "$(CYAN)$(BOLD)🔄 Restarting app and monitoring stack in development environment...$(RESET)"
	docker compose -f docker/development/docker-compose.yml --env-file .env.development restart
	docker compose -f docker/monitoring/development/docker-compose.yml --env-file .env.development restart
	@echo "$(GREEN)✅ App and monitoring stack restarted in development environment.$(RESET)"
	@echo "$(CYAN)ℹ️  Grafana: http://localhost:3000 (admin/admin)$(RESET)"
	@echo "$(CYAN)ℹ️  Prometheus: http://localhost:9090$(RESET)"
	@echo "$(CYAN)ℹ️  Loki: http://localhost:3100$(RESET)"

# ======================================
# 🛠️  STAGING ENVIRONMENT
# ======================================
staging-build:
	@echo "$(YELLOW)$(BOLD)🚀 Building staging environment...$(RESET)"
	docker compose -f docker/staging/docker-compose.yml --env-file .env.staging build
	@echo "$(GREEN)✅ Staging environment built successfully.$(RESET)"

staging-up:
	@echo "$(YELLOW)$(BOLD)🚀 Starting staging environment...$(RESET)"
	docker compose -f docker/staging/docker-compose.yml --env-file .env.staging up -d
	@echo "$(GREEN)✅ Staging environment started successfully.$(RESET)"

staging-down:
	@echo "$(YELLOW)$(BOLD)🛑 Stopping staging environment...$(RESET)"
	docker compose -f docker/staging/docker-compose.yml --env-file .env.staging down
	@echo "$(GREEN)✅ Staging environment stopped successfully.$(RESET)"

staging-restart:
	@echo "$(YELLOW)$(BOLD)🔄 Restarting staging environment...$(RESET)"
	docker compose -f docker/staging/docker-compose.yml --env-file .env.staging restart
	@echo "$(GREEN)✅ Staging environment restarted successfully.$(RESET)"

staging-logs:
	@echo "$(YELLOW)$(BOLD)📋 Viewing staging logs...$(RESET)"
	docker compose -f docker/staging/docker-compose.yml --env-file .env.staging logs -f

staging-migrate:
	@echo "$(YELLOW)$(BOLD)🔧 Running migrations in staging environment...$(RESET)"
	docker compose -f docker/staging/docker-compose.yml --env-file .env.staging run --rm backend python manage.py migrate
	@echo "$(GREEN)✅ Migrations applied successfully.$(RESET)"

staging-collectstatic:
	@echo "$(YELLOW)$(BOLD)🔧 Collecting static files in staging environment...$(RESET)"
	docker compose -f docker/staging/docker-compose.yml --env-file .env.staging run --rm backend python manage.py collectstatic --no-input
	@echo "$(GREEN)✅ Static files collected successfully.$(RESET)"

# ======================================
# 📊 MONITORING - STAGING
# ======================================
monitoring-staging-up:
	@echo "$(MAGENTA)$(BOLD)📊 Starting monitoring stack in staging environment...$(RESET)"
	docker compose -f docker/monitoring/staging/docker-compose.yml --env-file .env.staging up -d
	@echo "$(GREEN)✅ Monitoring stack started in staging environment.$(RESET)"
	@echo "$(CYAN)ℹ️  Grafana: http://localhost:3000 (admin/StrongStaginPassword123!)$(RESET)"
	@echo "$(CYAN)ℹ️  Prometheus: http://localhost:9090$(RESET)"
	@echo "$(CYAN)ℹ️  Loki: http://localhost:3100$(RESET)"

monitoring-staging-down:
	@echo "$(MAGENTA)$(BOLD)🛑 Stopping monitoring stack in staging environment...$(RESET)"
	docker compose -f docker/monitoring/staging/docker-compose.yml --env-file .env.staging down
	@echo "$(GREEN)✅ Monitoring stack stopped in staging environment.$(RESET)"

monitoring-staging-restart:
	@echo "$(MAGENTA)$(BOLD)🔄 Restarting monitoring stack in staging environment...$(RESET)"
	docker compose -f docker/monitoring/staging/docker-compose.yml --env-file .env.staging restart
	@echo "$(GREEN)✅ Monitoring stack restarted in staging environment.$(RESET)"

monitoring-staging-logs:
	@echo "$(MAGENTA)$(BOLD)📋 Viewing monitoring logs in staging environment...$(RESET)"
	docker compose -f docker/monitoring/staging/docker-compose.yml --env-file .env.staging logs -f

monitoring-staging-status:
	@echo "$(MAGENTA)$(BOLD)📋 Checking monitoring status in staging environment...$(RESET)"
	docker compose -f docker/monitoring/staging/docker-compose.yml --env-file .env.staging ps

# ======================================
# 🔄 COMBINED STAGING TARGETS
# ======================================
staging-all-up:
	@echo "$(CYAN)$(BOLD)🚀 Starting app and monitoring stack in staging environment...$(RESET)"
	docker compose -f docker/staging/docker-compose.yml --env-file .env.staging up -d
	docker compose -f docker/monitoring/staging/docker-compose.yml --env-file .env.staging up -d
	@echo "$(GREEN)✅ App and monitoring stack started in staging environment.$(RESET)"
	@echo "$(CYAN)ℹ️  Grafana: http://localhost:3000 (admin/StrongStaginPassword123!)$(RESET)"
	@echo "$(CYAN)ℹ️  Prometheus: http://localhost:9090$(RESET)"
	@echo "$(CYAN)ℹ️  Loki: http://localhost:3100$(RESET)"

staging-all-down:
	@echo "$(CYAN)$(BOLD)🛑 Stopping app and monitoring stack in staging environment...$(RESET)"
	docker compose -f docker/staging/docker-compose.yml --env-file .env.staging down
	docker compose -f docker/monitoring/staging/docker-compose.yml --env-file .env.staging down
	@echo "$(GREEN)✅ App and monitoring stack stopped in staging environment.$(RESET)"

staging-all-restart:
	@echo "$(CYAN)$(BOLD)🔄 Restarting app and monitoring stack in staging environment...$(RESET)"
	docker compose -f docker/staging/docker-compose.yml --env-file .env.staging restart
	docker compose -f docker/monitoring/staging/docker-compose.yml --env-file .env.staging restart
	@echo "$(GREEN)✅ App and monitoring stack restarted in staging environment.$(RESET)"
	@echo "$(CYAN)ℹ️  Grafana: http://localhost:3000 (admin/StrongStaginPassword123!)$(RESET)"
	@echo "$(CYAN)ℹ️  Prometheus: http://localhost:9090$(RESET)"
	@echo "$(CYAN)ℹ️  Loki: http://localhost:3100$(RESET)"

# ======================================
# 🛠️  PRODUCTION ENVIRONMENT
# ======================================
production-build:
	@echo "$(RED)$(BOLD)🚀 Building production environment...$(RESET)"
	docker compose -f docker/production/docker-compose.yml --env-file .env.production build
	@echo "$(GREEN)✅ Production environment built successfully.$(RESET)"

production-up:
	@echo "$(RED)$(BOLD)🚀 Starting production environment...$(RESET)"
	docker compose -f docker/production/docker-compose.yml --env-file .env.production up -d
	@echo "$(GREEN)✅ Production environment started successfully.$(RESET)"

production-down:
	@echo "$(RED)$(BOLD)🛑 Stopping production environment...$(RESET)"
	docker compose -f docker/production/docker-compose.yml --env-file .env.production down
	@echo "$(GREEN)✅ Production environment stopped successfully.$(RESET)"

production-restart:
	@echo "$(RED)$(BOLD)🔄 Restarting production environment...$(RESET)"
	docker compose -f docker/production/docker-compose.yml --env-file .env.production restart
	@echo "$(GREEN)✅ Production environment restarted successfully.$(RESET)"

production-logs:
	@echo "$(RED)$(BOLD)📋 Viewing production logs...$(RESET)"
	docker compose -f docker/production/docker-compose.yml --env-file .env.production logs -f

production-migrate:
	@echo "$(RED)$(BOLD)🔧 Running migrations in production environment...$(RESET)"
	docker compose -f docker/production/docker-compose.yml --env-file .env.production run --rm backend python manage.py migrate
	@echo "$(GREEN)✅ Migrations applied successfully.$(RESET)"

production-collectstatic:
	@echo "$(RED)$(BOLD)🔧 Collecting static files in production environment...$(RESET)"
	docker compose -f docker/production/docker-compose.yml --env-file .env.production run --rm backend python manage.py collectstatic --no-input
	@echo "$(GREEN)✅ Static files collected successfully.$(RESET)"

# ======================================
# 📊 MONITORING - PRODUCTION
# ======================================
monitoring-production-up:
	@echo "$(MAGENTA)$(BOLD)📊 Starting monitoring stack in production environment...$(RESET)"
	docker compose -f docker/monitoring/production/docker-compose.yml --env-file .env.production up -d
	@echo "$(GREEN)✅ Monitoring stack started in production environment.$(RESET)"
	@echo "$(CYAN)ℹ️  Grafana: http://localhost:3000 (admin/set via GRAFANA_ADMIN_PASSWORD)$(RESET)"
	@echo "$(CYAN)ℹ️  Prometheus: http://localhost:9090$(RESET)"
	@echo "$(CYAN)ℹ️  Loki: http://localhost:3100$(RESET)"

monitoring-production-down:
	@echo "$(MAGENTA)$(BOLD)🛑 Stopping monitoring stack in production environment...$(RESET)"
	docker compose -f docker/monitoring/production/docker-compose.yml --env-file .env.production down
	@echo "$(GREEN)✅ Monitoring stack stopped in production environment.$(RESET)"

monitoring-production-restart:
	@echo "$(MAGENTA)$(BOLD)🔄 Restarting monitoring stack in production environment...$(RESET)"
	docker compose -f docker/monitoring/production/docker-compose.yml --env-file .env.production restart
	@echo "$(GREEN)✅ Monitoring stack restarted in production environment.$(RESET)"

monitoring-production-logs:
	@echo "$(MAGENTA)$(BOLD)📋 Viewing monitoring logs in production environment...$(RESET)"
	docker compose -f docker/monitoring/production/docker-compose.yml --env-file .env.production logs -f

monitoring-production-status:
	@echo "$(MAGENTA)$(BOLD)📋 Checking monitoring status in production environment...$(RESET)"
	docker compose -f docker/monitoring/production/docker-compose.yml --env-file .env.production ps

# ======================================
# 🔄 COMBINED PRODUCTION TARGETS
# ======================================
production-all-up:
	@echo "$(CYAN)$(BOLD)🚀 Starting app and monitoring stack in production environment...$(RESET)"
	docker compose -f docker/production/docker-compose.yml --env-file .env.production up -d
	docker compose -f docker/monitoring/production/docker-compose.yml --env-file .env.production up -d
	@echo "$(GREEN)✅ App and monitoring stack started in production environment.$(RESET)"
	@echo "$(CYAN)ℹ️  Grafana: http://localhost:3000 (admin/set via GRAFANA_ADMIN_PASSWORD)$(RESET)"
	@echo "$(CYAN)ℹ️  Prometheus: http://localhost:9090$(RESET)"
	@echo "$(CYAN)ℹ️  Loki: http://localhost:3100$(RESET)"

production-all-down:
	@echo "$(CYAN)$(BOLD)🛑 Stopping app and monitoring stack in production environment...$(RESET)"
	docker compose -f docker/production/docker-compose.yml --env-file .env.production down
	docker compose -f docker/monitoring/production/docker-compose.yml --env-file .env.production down
	@echo "$(GREEN)✅ App and monitoring stack stopped in production environment.$(RESET)"

production-all-restart:
	@echo "$(CYAN)$(BOLD)🔄 Restarting app and monitoring stack in production environment...$(RESET)"
	docker compose -f docker/production/docker-compose.yml --env-file .env.production restart
	docker compose -f docker/monitoring/production/docker-compose.yml --env-file .env.production restart
	@echo "$(GREEN)✅ App and monitoring stack restarted in production environment.$(RESET)"
	@echo "$(CYAN)ℹ️  Grafana: http://localhost:3000 (admin/set via GRAFANA_ADMIN_PASSWORD)$(RESET)"
	@echo "$(CYAN)ℹ️  Prometheus: http://localhost:9090$(RESET)"
	@echo "$(CYAN)ℹ️  Loki: http://localhost:3100$(RESET)"

# ======================================
# 🧪 TESTING
# ======================================
test:
	@echo "$(BLUE)$(BOLD)🧪 Running tests...$(RESET)"
	docker compose -f docker/development/docker-compose.yml --env-file .env.development run --rm backend python manage.py test
	@echo "$(GREEN)✅ Tests completed.$(RESET)"

test-coverage:
	@echo "$(BLUE)$(BOLD)🧪 Running tests with coverage...$(RESET)"
	docker compose -f docker/development/docker-compose.yml --env-file .env.development run --rm backend coverage run manage.py test
	docker compose -f docker/development/docker-compose.yml --env-file .env.development run --rm backend coverage report
	@echo "$(GREEN)✅ Coverage report generated.$(RESET)"

# ======================================
# 💾 DATABASE
# ======================================
db-backup:
	@echo "$(YELLOW)$(BOLD)💾 Creating database backup...$(RESET)"
	docker compose -f docker/production/docker-compose.yml --env-file .env.production exec db pg_dump -U personal_production personal_production > backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "$(GREEN)✅ Database backup created successfully: backup_$(shell date +%Y%m%d_%H%M%S).sql$(RESET)"

db-restore:
	@echo "$(YELLOW)$(BOLD)💾 Restoring database from $(file)...$(RESET)"
	docker compose -f docker/production/docker-compose.yml --env-file .env.production exec -T db psql -U personal_production personal_production < $(file)
	@echo "$(GREEN)✅ Database restored successfully from $(file).$(RESET)"

# ======================================
# 🧹 CLEANUP
# ======================================
clean:
	@echo "$(RED)$(BOLD)🧹 Cleaning unused Docker resources...$(RESET)"
	docker system prune -f
	docker volume prune -f
	@echo "$(GREEN)✅ Unused Docker resources cleaned successfully.$(RESET)"

clean-all:
	@echo "$(RED)$(BOLD)⚠️  WARNING: This will remove ALL Docker containers, images, volumes, and networks ⚠️$(RESET)"
	@echo "$(RED)Are you sure you want to continue? [y/N] $(RESET)" && read ans && [ $${ans:-N} = y ]
	@echo "$(RED)$(BOLD)🧹 Stopping all containers...$(RESET)"
	@docker stop $$(docker ps -aq) 2>/dev/null || true
	@echo "$(RED)$(BOLD)🧹 Removing all containers...$(RESET)"
	@docker rm $$(docker ps -aq) 2>/dev/null || true
	@echo "$(RED)$(BOLD)🧹 Removing all images...$(RESET)"
	@docker rmi $$(docker images -q) --force 2>/dev/null || true
	@echo "$(RED)$(BOLD)🧹 Removing all volumes...$(RESET)"
	@docker volume rm $$(docker volume ls -q) 2>/dev/null || true
	@echo "$(RED)$(BOLD)🧹 Removing all networks...$(RESET)"
	@docker network rm $$(docker network ls -q) 2>/dev/null || true
	@echo "$(GREEN)✅ All Docker resources have been removed!$(RESET)"

# ======================================
# ℹ️ HELP
# ======================================
help:
	@echo "$(BOLD)$(CYAN)╔═════════════════════════════════════════════════════════════════════════════╗$(RESET)"
	@echo "$(BOLD)$(CYAN)║                            AVAILABLE COMMANDS                               ║$(RESET)"
	@echo "$(BOLD)$(CYAN)╚═════════════════════════════════════════════════════════════════════════════╝$(RESET)"
	@echo ""
	@echo "$(BOLD)$(BLUE)DEVELOPMENT:$(RESET)"
	@echo "  $(BOLD)development-build$(RESET)             - 🚀 Build development environment"
	@echo "  $(BOLD)development-up$(RESET)                - 🚀 Start development environment"
	@echo "  $(BOLD)development-up-d$(RESET)              - 🚀 Start development environment in detached mode"
	@echo "  $(BOLD)development-down$(RESET)              - 🛑 Stop development environment"
	@echo "  $(BOLD)development-restart$(RESET)           - 🔄 Restart development environment"
	@echo "  $(BOLD)development-logs$(RESET)              - 📋 View development logs"
	@echo "  $(BOLD)development-shell$(RESET)             - 🔧 Open Django shell"
	@echo "  $(BOLD)development-migrate$(RESET)           - 🔧 Run migrations"
	@echo "  $(BOLD)development-makemigrations$(RESET)    - 🔧 Create new migrations"
	@echo "  $(BOLD)development-createsuperuser$(RESET)   - 👤 Create superuser"
	@echo "  $(BOLD)development-all-up$(RESET)            - 🚀 Start both app and monitoring in development"
	@echo "  $(BOLD)development-all-down$(RESET)          - 🛑 Stop both app and monitoring in development"
	@echo "  $(BOLD)development-all-restart$(RESET)       - 🔄 Restart both app and monitoring in development"
	@echo ""
	@echo "$(BOLD)$(YELLOW)STAGING:$(RESET)"
	@echo "  $(BOLD)staging-build$(RESET)                 - 🚀 Build staging environment"
	@echo "  $(BOLD)staging-up$(RESET)                    - 🚀 Start staging environment"
	@echo "  $(BOLD)staging-down$(RESET)                  - 🛑 Stop staging environment"
	@echo "  $(BOLD)staging-restart$(RESET)               - 🔄 Restart staging environment"
	@echo "  $(BOLD)staging-logs$(RESET)                  - 📋 View staging logs"
	@echo "  $(BOLD)staging-migrate$(RESET)               - 🔧 Run migrations"
	@echo "  $(BOLD)staging-collectstatic$(RESET)         - 🔧 Collect static files"
	@echo "  $(BOLD)staging-all-up$(RESET)                - 🚀 Start both app and monitoring in staging"
	@echo "  $(BOLD)staging-all-down$(RESET)              - 🛑 Stop both app and monitoring in staging"
	@echo "  $(BOLD)staging-all-restart$(RESET)           - 🔄 Restart both app and monitoring in staging"
	@echo ""
	@echo "$(BOLD)$(RED)PRODUCTION:$(RESET)"
	@echo "  $(BOLD)production-build$(RESET)              - 🚀 Build production environment"
	@echo "  $(BOLD)production-up$(RESET)                 - 🚀 Start production environment"
	@echo "  $(BOLD)production-down$(RESET)               - 🛑 Stop production environment"
	@echo "  $(BOLD)production-restart$(RESET)            - 🔄 Restart production environment"
	@echo "  $(BOLD)production-logs$(RESET)               - 📋 View production logs"
	@echo "  $(BOLD)production-migrate$(RESET)            - 🔧 Run migrations"
	@echo "  $(BOLD)production-collectstatic$(RESET)      - 🔧 Collect static files"
	@echo "  $(BOLD)production-all-up$(RESET)             - 🚀 Start both app and monitoring in production"
	@echo "  $(BOLD)production-all-down$(RESET)           - 🛑 Stop both app and monitoring in production"
	@echo "  $(BOLD)production-all-restart$(RESET)        - 🔄 Restart both app and monitoring in production"
	@echo ""
	@echo "$(BOLD)$(MAGENTA)MONITORING:$(RESET)"
	@echo "  $(BOLD)Development:$(RESET)"
	@echo "    $(BOLD)monitoring-development-up$(RESET)           - 📊 Start monitoring stack in development"
	@echo "    $(BOLD)monitoring-development-down$(RESET)         - 🛑 Stop monitoring stack in development"
	@echo "    $(BOLD)monitoring-development-restart$(RESET)      - 🔄 Restart monitoring stack in development"
	@echo "    $(BOLD)monitoring-development-logs$(RESET)         - 📋 View monitoring logs in development"
	@echo "    $(BOLD)monitoring-development-status$(RESET)       - 📋 Check monitoring status in development"
	@echo ""
	@echo "  $(BOLD)Staging:$(RESET)"
	@echo "    $(BOLD)monitoring-staging-up$(RESET)               - 📊 Start monitoring stack in staging"
	@echo "    $(BOLD)monitoring-staging-down$(RESET)             - 🛑 Stop monitoring stack in staging"
	@echo "    $(BOLD)monitoring-staging-restart$(RESET)          - 🔄 Restart monitoring stack in staging"
	@echo "    $(BOLD)monitoring-staging-logs$(RESET)             - 📋 View monitoring logs in staging"
	@echo "    $(BOLD)monitoring-staging-status$(RESET)           - 📋 Check monitoring status in staging"
	@echo ""
	@echo "  $(BOLD)Production:$(RESET)"
	@echo "    $(BOLD)monitoring-production-up$(RESET)            - 📊 Start monitoring stack in production"
	@echo "    $(BOLD)monitoring-production-down$(RESET)          - 🛑 Stop monitoring stack in production"
	@echo "    $(BOLD)monitoring-production-restart$(RESET)       - 🔄 Restart monitoring stack in production"
	@echo "    $(BOLD)monitoring-production-logs$(RESET)          - 📋 View monitoring logs in production"
	@echo "    $(BOLD)monitoring-production-status$(RESET)        - 📋 Check monitoring status in production"
	@echo ""
	@echo "$(BOLD)$(BLUE)TESTING:$(RESET)"
	@echo "  $(BOLD)test$(RESET)                          - 🧪 Run tests"
	@echo "  $(BOLD)test-coverage$(RESET)                 - 🧪 Run tests with coverage report"
	@echo ""
	@echo "$(BOLD)$(YELLOW)DATABASE:$(RESET)"
	@echo "  $(BOLD)db-backup$(RESET)                     - 💾 Backup production database"
	@echo "  $(BOLD)db-restore file=<filename>$(RESET)    - 💾 Restore database from backup"
	@echo ""
	@echo "$(BOLD)$(RED)CLEANUP:$(RESET)"
	@echo "  $(BOLD)clean$(RESET)                         - 🧹 Clean unused Docker resources (dangling images, stopped containers)"
	@echo "  $(BOLD)clean-all$(RESET)                     - 🧹 Remove ALL Docker containers, images, volumes, and networks (use with caution!)"
	@echo ""
	@echo "$(CYAN)Use 'make <command>' to run a specific command.$(RESET)"
