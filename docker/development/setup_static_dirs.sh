#!/bin/bash
# Source environment variables from .env.development
set -a
source ../../.env.development
set +a

# Create directories
mkdir -p ${PROJECT_STATIC_ROOT}
mkdir -p ${PROJECT_MEDIA_ROOT}

# Set permissions
chmod -R 755 ${PROJECT_STATIC_ROOT}
chmod -R 755 ${PROJECT_MEDIA_ROOT} 