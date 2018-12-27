"""Django settings for tests."""

import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# Quick-start development settings - unsuitable for production

SECRET_KEY = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

INTERNAL_IPS = ['127.0.0.1']

LOGGING_CONFIG = None   # avoids spurious output in tests

# Application definition

INSTALLED_APPS = [
    'channels',
    'plantgrower',
    'tests'
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True
    },
]

ROOT_URLCONF = 'tests.urls'

STATIC_URL = 'plantgrower/static/'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

USE_TZ = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
