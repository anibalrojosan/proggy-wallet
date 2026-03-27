#!/usr/bin/env bash
# build.sh — Build script for Render

set -o errexit    # Stop if there is an error

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Apply migrations
python manage.py migrate

# Show migrations status (to verify DB health)
python manage.py showmigrations