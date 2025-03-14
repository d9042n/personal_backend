# Logging System

This directory contains the application logs for the personal backend project. The logs are organized in a date-based directory structure.

## Structure

```
logs/
├── YYYY-MM-DD/          # Date-based directory (e.g., 2025-03-13/)
│   ├── info.log         # Information level logs
│   ├── error.log        # Error level logs
│   └── debug.log        # Debug level logs (only in development)
├── README.md            # This file
└── ...
```

## Log Files

The application uses a custom `DailyDirectoryLogHandler` which organizes logs into date-based directories. Each directory contains:

- **info.log** - Contains all INFO-level logs
- **error.log** - Contains ERROR and CRITICAL level logs
- **debug.log** - Contains DEBUG-level logs (only available in development/debug mode)

## Monitoring Integration

The logs are monitored using Grafana Loki and Promtail. The monitoring setup is configured in the `docker/monitoring` directory.

### How Logs are Collected

1. **Promtail** collects logs from the date-based directories
2. Logs are sent to **Loki** for storage and indexing
3. **Grafana** dashboards visualize the logs with custom filters and panels

### Viewing Logs

You can view your logs in several ways:

1. **Directly**: By browsing the date-based directories and viewing the log files
2. **Grafana**: By accessing the Grafana dashboard at http://localhost:3000
   - Use the "Django Application Logs" dashboard for a comprehensive view

## Log Format

Logs use the following standard format:

```
YYYY-MM-DD HH:MM:SS,mmm LEVEL MODULE PROCESS_ID THREAD_ID MESSAGE
```

For example:

```
2025-03-13 09:48:01,697 INFO apps 1 281473305165856 Initializing Users app
```

## Retention Policy

Log files are kept for 30 days for info and error logs, and 7 days for debug logs, after which they are automatically rotated and old logs are removed.

## Adding New Loggers

When adding new modules or apps to the project, add appropriate loggers in `settings.py` following the established pattern:

```python
'new_app_name': {
    'handlers': ['console', 'file_info', 'file_error', 'file_debug'],
    'level': 'DEBUG' if DEBUG else 'INFO',
    'propagate': True,
},
```
