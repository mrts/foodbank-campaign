"""
Django settings for foodbank project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import platform

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# -> this *MUST BE OVERRIDEN* with settings_local in production
SECRET_KEY = 'e6#83hi)*reeq2lk1v9y59u(z@i7(wto-ter#q&3ii8f6t8n2x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'osale.toidupank.ee',
    'test-osale.toidupank.ee',
    'uus-osale.toidupank.ee',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tinymce',
    'nested_admin',
    'locations',
    'campaigns',
    'coordinators',
    'volunteers',
    'auditlog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'foodbank.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'foodbank.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'et-ee'

TIME_ZONE = 'Europe/Tallinn'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

HTDOCS = os.path.join(BASE_DIR, '..', 'htdocs')

STATIC_URL  = '/static/media/'
STATIC_ROOT = os.path.join(HTDOCS, 'static', 'media')

MEDIA_URL   = '/static/uploads/'
MEDIA_ROOT  = os.path.join(HTDOCS, 'static', 'uploads')

# Rich-text editor

TINYMCE_DEFAULT_CONFIG = {
    'plugins': 'link lists code',
    'menubar': 'edit format',
    'toolbar': 'undo redo | styleselect | bold italic | removeformat | link | bullist numlist | code',
    'width': 500,
    'height': 400,
}

# Fix Estonian date formatting
FORMAT_MODULE_PATH = 'foodbank.formats'

EMAIL_BACKEND = 'django_sendmail_backend.backends.EmailBackend'
# For testing email:
# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# EMAIL_FILE_PATH = '/tmp/toidupank-email-messages'

ADMIN_URL_PREFIX = 'haldus/'

# Mandatory settings override in production environment
PRODUCTION_HOSTNAME = 'atria.elkdata.ee'
IS_PRODUCTION_ENV = False
if platform.node() == PRODUCTION_HOSTNAME and 'live-osale' in BASE_DIR:
    IS_PRODUCTION_ENV = True
    from .settings_live import *
else:
    # Optional local settings override, especially useful during development
    try:
        from .settings_local import *
    except ImportError:
        pass
