"""
Django settings for Blog project.

Updated for Vercel Deployment (Crash-Proof Database Config).
"""

import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================================================================
#  SECURITY
# ==============================================================================

# Vercel provides 'VERCEL' env var. If present, we turn off Debug.
DEBUG = 'VERCEL' not in os.environ

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-local-dev-key')

ALLOWED_HOSTS = ['.vercel.app', '.now.sh', 'localhost', '127.0.0.1']

# ==============================================================================
#  APPS & MIDDLEWARE
# ==============================================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    'users',
    'home',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'Blog.wsgi.application'

# ==============================================================================
#  DATABASE (CRASH-PROOF FIX)
# ==============================================================================

import dj_database_url

# 1. Default to SQLite (Works for build process)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 2. Try to load the Production Database
# We wrap this in a TRY block so it NEVER crashes the build, 
# even if the URL is empty, broken, or garbage.
try:
    database_url = os.environ.get('DATABASE_URL')
    # Check if it looks like a real URL (longer than 10 chars)
    if database_url and len(database_url) > 10:
        prod_db = dj_database_url.parse(
            database_url,
            conn_max_age=600,
            ssl_require=False
        )
        DATABASES['default'] = prod_db
except Exception as e:
    # If anything goes wrong, just print a warning and keep using SQLite
    print(f"WARNING: Could not load DATABASE_URL. Using SQLite. Error: {e}")

# ==============================================================================
#  STATIC FILES
# ==============================================================================

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = []
if (BASE_DIR / 'static').exists():
    STATICFILES_DIRS.append(BASE_DIR / 'static')

# Enable WhiteNoise for serving static files on Vercel
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ==============================================================================
#  I18N & DEFAULT AUTO FIELD
# ==============================================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'