#!/bin/bash
# Source environment variables from .env.staging
set -a
source ../../.env.staging
set +a

# Create directories
sudo mkdir -p ${PROJECT_STATIC_ROOT}
sudo mkdir -p ${PROJECT_MEDIA_ROOT}

# Set permissions
sudo chown -R www-data:www-data ${PROJECT_STATIC_ROOT}
sudo chown -R www-data:www-data ${PROJECT_MEDIA_ROOT}
sudo chmod -R 755 ${PROJECT_STATIC_ROOT}
sudo chmod -R 755 ${PROJECT_MEDIA_ROOT} 