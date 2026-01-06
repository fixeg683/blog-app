#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# 1. Run Migrations
echo "Applying database migrations..."
python manage.py migrate

# 2. Start the Server
echo "Starting Gunicorn..."
exec gunicorn Blog.wsgi:application --bind 0.0.0.0:10000