"""
Django settings for Blog project.

Updated for deployment on Vercel.
"""

import os
from pathlib import Path
import dj_database_url  # Required for connecting to external databases (Render/Neon/Supabase)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================================================================
#  SECURITY SETTINGS
# ==============================================================================

# Get SECRET_KEY from environment. 
# On Vercel: Set this in the Project Settings > Environment Variables.
# Locally: It falls back to the insecure key for development.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-local-dev-key-change-me')

# DEBUG Logic:
# Vercel sets a 'VERCEL' environment variable. If found, DEBUG is False.
# Locally, it defaults to True.
DEBUG = 'VERCEL' not in os.environ

# ALLOWED_HOSTS:
# 1. '.vercel.app' -> Allows any Vercel subdomain
# 2. 'localhost'/'127.0.0.1' -> Allows local testing
ALLOWED_HOSTS = ['.vercel.app', '.now.sh', 'localhost', '127.0.0.1']


# ==============================================================================
#  APPLICATION DEFINITION
# ==============================================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Your Custom Apps
    'blog',
    'users',
    'home',  # Ensure all your apps are listed here
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    
    # WhiteNoise is CRITICAL for Vercel. 
    # It allows Django to serve its own static files (CSS/JS) efficiently.
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
#  DATABASE CONFIGURATION
# ==============================================================================

# Vercel has a Read-Only filesystem, so you CANNOT use SQLite there.
# This logic checks for a DATABASE_URL. 
# - If found (Vercel): Connects to Postgres.
# - If not found (Local): Connects to SQLite.

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'),
        conn_max_age=600,
        ssl_require=False  # Set to True if your DB provider requires SSL (e.g., Heroku/Neon)
    )
}


# ==============================================================================
#  PASSWORD VALIDATION
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ==============================================================================
#  INTERNATIONALIZATION
# ==============================================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ==============================================================================
#  STATIC FILES (CSS, JavaScript, Images)
# ==============================================================================

STATIC_URL = 'static/'

# Where collectstatic puts files for deployment
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Where you keep your static files during development
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Enable WhiteNoise compression and caching support
# This makes your site load faster on Vercel
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ==============================================================================
#  DEFAULT PRIMARY KEY FIELD TYPE
# ==============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'