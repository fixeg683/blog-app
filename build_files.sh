#!/bin/bash

# Exit on error
set -e

echo "Ensuring pip is available..."
# 1. Install pip using ensurepip (just in case it's missing)
python3.9 -m ensurepip --upgrade

echo "Installing requirements..."
# 2. Install dependencies
python3.9 -m pip install -r requirements.txt

echo "Collecting static files..."
# 3. Collect static files
python3.9 manage.py collectstatic --noinput --clear