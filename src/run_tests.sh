#!/bin/sh
set -e
coverage run manage.py test --settings=django_invest.settings.test
coverage report
