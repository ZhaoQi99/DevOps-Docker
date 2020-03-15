from datetime import timedelta

from .base import *

DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ops',
        'USER': 'postgres',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

AUTH_CONFIG['AUTH_TOKEN_EXPIRE'] = timedelta(days=10)
MIDDLEWARE.pop(5)  # CSRF
