#!/bin/sh
+ set -eux
set -e

# Create .netrc file for git HTTPS auth using Render environment variable
if [ -n "$GITHUB_TOKEN" ]; then
  echo "machine github.com" > ~/.netrc
  echo "login oauth2" >> ~/.netrc
  echo "password $GITHUB_TOKEN" >> ~/.netrc
  chmod 600 ~/.netrc
fi

# Upgrade pip and install dependencies from requirements.txt
pip install --upgrade pip
pip install -r requirements.txt

# Run Django management commands
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate

# Execute the CMD from Dockerfile (starts gunicorn)
exec "$@"
