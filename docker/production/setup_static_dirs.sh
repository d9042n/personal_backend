#!/bin/bash
# Source environment variables from .env.production
set -a
source ../../.env.production
set +a

# Create directories
sudo mkdir -p ${PROJECT_STATIC_ROOT}
sudo mkdir -p ${PROJECT_MEDIA_ROOT}
sudo mkdir -p ${APP_LOGS_PATH}

# Set permissions
sudo chown -R www-data:www-data ${PROJECT_STATIC_ROOT}
sudo chown -R www-data:www-data ${PROJECT_MEDIA_ROOT}
sudo chown -R www-data:www-data ${APP_LOGS_PATH}
sudo chmod -R 755 ${PROJECT_STATIC_ROOT}
sudo chmod -R 755 ${PROJECT_MEDIA_ROOT}
sudo chmod -R 755 ${APP_LOGS_PATH} 