#!/bin/sh

set -e

. /venv/bin/activate

python manage.py makemigrations
python manage.py migrate
#python manage.py initiate_admin
#python manage.py collectstatic
exec python manage.py runserver 0.0.0.0:8000
#exec gunicorn django_invest.wsgi:application --bind 0.0.0.0:8000
