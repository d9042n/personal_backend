# Monitoring Stack

This directory contains the monitoring stack setup for the personal backend project. The monitoring setup uses the Loki stack, which includes:

- **Prometheus**: For metrics collection
- **Loki**: For log aggregation
- **Promtail**: For log shipping
- **Grafana**: For visualization

## Directory Structure

```
monitoring/
├── common/                # Common configuration shared across environments
│   ├── docker-compose.yml # Base docker-compose file
│   ├── prometheus/        # Prometheus configuration
│   ├── loki/              # Loki configuration
│   ├── promtail/          # Promtail configuration
│   └── grafana/           # Grafana configuration and dashboards
├── development/           # Development environment specific files
│   └── docker-compose.yml # Development docker-compose file
├── staging/               # Staging environment specific files
│   └── docker-compose.yml # Staging docker-compose file
├── production/            # Production environment specific files
│   └── docker-compose.yml # Production docker-compose file
└── README.md              # This file
```

## Environment-Specific Configurations

All environments use the same standard ports to ensure consistent datasource configurations:

- Prometheus: 9090
- Loki: 3100
- Grafana: 3000

### Development Environment

- Basic configurations with default admin credentials (admin/admin)

### Staging Environment

- More secure admin credentials (admin/StrongStaginPassword123!)

### Production Environment

- Enhanced security settings
- Uses environment variables for sensitive data
- Production-grade logging configurations
- Always restart policy

## Usage

### Using the Makefile

The monitoring stack can be easily managed using the project's Makefile. Here are the available commands:

```bash
# Development environment
make monitoring-dev-up      # Start monitoring in development
make monitoring-dev-down    # Stop monitoring in development
make monitoring-dev-restart # Restart monitoring in development
make monitoring-dev-logs    # View monitoring logs in development
make monitoring-dev-status  # Check monitoring status in development

# Staging environment
make monitoring-staging-up      # Start monitoring in staging
make monitoring-staging-down    # Stop monitoring in staging
make monitoring-staging-restart # Restart monitoring in staging
make monitoring-staging-logs    # View monitoring logs in staging
make monitoring-staging-status  # Check monitoring status in staging

# Production environment
make monitoring-prod-up      # Start monitoring in production
make monitoring-prod-down    # Stop monitoring in production
make monitoring-prod-restart # Restart monitoring in production
make monitoring-prod-logs    # View monitoring logs in production
make monitoring-prod-status  # Check monitoring status in production

# Combined commands (app + monitoring)
make development-all-up    # Start both app and monitoring in development
make development-all-down  # Stop both app and monitoring in development
make staging-all-up        # Start both app and monitoring in staging
make staging-all-down      # Stop both app and monitoring in staging
make production-all-up     # Start both app and monitoring in production
make production-all-down   # Stop both app and monitoring in production
```

### Manual Usage

If you prefer not to use the Makefile, you can manually manage the monitoring stack:

```bash
# For development
cd docker/monitoring/development
docker-compose up -d     # Start
docker-compose down      # Stop
docker-compose restart   # Restart
docker-compose logs -f   # View logs
docker-compose ps        # Check status

# Similar commands for staging and production
```

### Accessing Grafana

Once the stack is running, you can access Grafana at http://localhost:3000 in all environments.

Default login:

- Username: admin
- Password:
  - Development: admin
  - Staging: StrongStaginPassword123!
  - Production: Set via environment variable GRAFANA_ADMIN_PASSWORD (defaults to StrongProductionPassword456!)

### Pre-configured Dashboards

The following dashboards are pre-configured and available in Grafana:

1. **Docker Metrics**: Shows container CPU and memory usage
2. **Loki Logs**: Shows system and Docker container logs

## Customizing

### Adding Custom Dashboards

To add custom dashboards:

1. Create a JSON dashboard file in `common/grafana/provisioning/dashboards/json/`
2. The dashboard will be automatically loaded when Grafana starts

### Adding Prometheus Scrape Targets

To monitor additional services:

1. Edit `common/prometheus/config/prometheus.yml`
2. Add a new job under the `scrape_configs` section

### Adding Promtail Log Sources

To collect logs from additional sources:

1. Edit `common/promtail/config/promtail-config.yml`
2. Add a new job under the `scrape_configs` section

## Django Application Logs

The monitoring stack is configured to collect and display Django application logs. These logs are stored in a date-based directory structure (`YYYY-MM-DD/filename.log`).

### Log Collection

The Promtail configuration includes a specific job for Django application logs:

```yaml
- job_name: django_application
  static_configs:
    - targets:
        - localhost
      labels:
        job: django
        app: personal_backend
        env: ${ENVIRONMENT:-development}
        __path__: /app/logs/*/*.log
  pipeline_stages:
    - regex:
        expression: '^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) (?P<level>\w+) (?P<module>\w+) (?P<process>\d+) (?P<thread>\d+) (?P<message>.*)$'
    - timestamp:
        source: timestamp
        format: "2006-01-02 15:04:05,000"
    - labels:
        level:
        module:
        process:
        thread:
    - output:
        source: message
```

This configuration:

1. Captures logs from date-based directories
2. Extracts metadata from log lines (timestamp, level, module, etc.)
3. Adds labels to make logs searchable and filterable in Grafana

### Django Logs Dashboard

The monitoring stack includes a pre-configured dashboard specifically for Django application logs:

- **Dashboard Name**: Django Application Logs
- **Location**: `common/grafana/provisioning/dashboards/json/django_logs_dashboard.json`

The dashboard provides:

- Log volume over time by level (ERROR, WARNING, INFO, DEBUG)
- Dedicated error logs panel
- Log distribution by module and level
- Searchable log explorer with level and module filters

### Environment-Specific Logs

The log collection automatically includes an `env` label based on the `ENVIRONMENT` variable. This allows you to filter logs by environment when using the same Loki instance for multiple deployments.

## Maintenance

### Backup Volumes

To backup the data volumes:

```bash
docker run --rm -v monitoring_prometheus_data:/source -v $(pwd)/backups:/backup alpine tar -czf /backup/prometheus-data.tar.gz -C /source .
docker run --rm -v monitoring_loki_data:/source -v $(pwd)/backups:/backup alpine tar -czf /backup/loki-data.tar.gz -C /source .
docker run --rm -v monitoring_grafana_data:/source -v $(pwd)/backups:/backup alpine tar -czf /backup/grafana-data.tar.gz -C /source .
```

### Restore Volumes

To restore from backups:

```bash
docker run --rm -v monitoring_prometheus_data:/target -v $(pwd)/backups:/backup alpine sh -c "rm -rf /target/* && tar -xzf /backup/prometheus-data.tar.gz -C /target"
docker run --rm -v monitoring_loki_data:/target -v $(pwd)/backups:/backup alpine sh -c "rm -rf /target/* && tar -xzf /backup/loki-data.tar.gz -C /target"
docker run --rm -v monitoring_grafana_data:/target -v $(pwd)/backups:/backup alpine sh -c "rm -rf /target/* && tar -xzf /backup/grafana-data.tar.gz -C /target"
```

## Best Practices

1. **Security**:

   - Use strong passwords in production
   - Limit access to the monitoring stack using network rules
   - Consider using TLS for production deployments

2. **Resource Management**:

   - Configure Prometheus retention based on server capacity
   - Monitor the disk usage of Loki and Prometheus
   - Consider adding resource limits in docker-compose

3. **High Availability**:

   - For mission-critical production deployments, consider a HA setup with multiple instances
   - Use a proper load balancer for production deployments

4. **Alerting**:
   - Configure Alertmanager in Prometheus for notifications
   - Set up appropriate alerting rules for critical metrics

## Troubleshooting

### Common Issues

1. **Prometheus can't scrape targets**:

   - Check network connectivity between containers
   - Verify target endpoints are accessible
   - Check Prometheus logs: `make monitoring-dev-logs` or `docker-compose logs prometheus`

2. **Loki can't receive logs**:

   - Check Promtail configuration
   - Verify Promtail has access to log files
   - Check Promtail and Loki logs

3. **Grafana can't connect to data sources**:
   - Verify data source configurations
   - Check network connectivity between containers
   - Restart Grafana: `docker-compose restart grafana`
