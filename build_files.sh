#!/bin/bash
set -e

echo "Ensuring pip is available..."
python3.9 -m ensurepip --upgrade

echo "Installing requirements..."
python3.9 -m pip install -r requirements.txt

echo "Collecting static files..."
python3.9 manage.py collectstatic --noinput --clear

echo "--- LIST OF COLLECTED STATIC FILES ---"
ls -R staticfiles
echo "--------------------------------------"