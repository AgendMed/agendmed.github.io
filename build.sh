#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

gunicorn AgendMed.wsgi:application --bind 0.0.0.0:$PORT
