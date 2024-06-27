#!/bin/bash
# exit on error
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input


python manage.py migrate
python manage.py runserver 0.0.0.0:8000