#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Run database migrations
echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

# Execute the command provided as CMD in the Dockerfile
exec "$@"
