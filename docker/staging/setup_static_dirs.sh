#!/bin/bash
# Create directories
sudo mkdir -p /var/www/personal/static
sudo mkdir -p /var/www/personal/media

# Set permissions
sudo chown -R www-data:www-data /var/www/personal/static
sudo chown -R www-data:www-data /var/www/personal/media
sudo chmod -R 755 /var/www/personal/static
sudo chmod -R 755 /var/www/personal/media 