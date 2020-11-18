from .base import *

DEBUG = True
TEMPLATES[0]["OPTIONS"]["context_processors"].append(
    "django.template.context_processors.debug"
)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        "NAME": "django_invest",  # Or path to database file if using sqlite3.
        "USER": "django_invest",  # Not used with sqlite3.
        "PASSWORD": "django_invest",  # Not used with sqlite3.
        "HOST": "",  # Set to empty string for localhost. Not used with sqlite3.
        "PORT": "",  # Set to empty string for default. Not used with sqlite3.
    }
}
