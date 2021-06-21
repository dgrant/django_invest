#!/usr/bin/env bash

set -e

rm -rf portfolio/migrations/*
rm -f db.sqlite3 
./manage.py makemigrations portfolio
./manage.py migrate
./manage.py import_csv ../TransactionHistory_22575818.csv "David Taxable Account"
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'davidgrant@gmail.com', 'admin')" | python manage.py shell
