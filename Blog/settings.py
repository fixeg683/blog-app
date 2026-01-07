"""
Django settings for Blog project.

Updated for Vercel Deployment.
"""

import os
from pathlib import Path
import dj_database_url  # Required for external DB connection

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
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Critical for static files
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
#  DATABASE
# ==============================================================================

# 1. Start with a default SQLite setup.
# This ensures 'collectstatic' works during the build even if the DB is missing.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 2. Check if a real database URL exists in the environment.
# We explicitly check for None or empty strings to prevent the "No support for ''" crash.
db_url = os.environ.get('DATABASE_URL')

if db_url and db_url.strip():
    # Only try to parse if the string is not empty
    import dj_database_url
    DATABASES['default'] = dj_database_url.parse(db_url, conn_max_age=600, ssl_require=False)

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