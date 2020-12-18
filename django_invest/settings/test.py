from .base import *

SECRET_KEY = "nx+c!vqd&=edi88mm43o_byvnh=ogf2%lt6%h@t9gzrvyw6$c*"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}
