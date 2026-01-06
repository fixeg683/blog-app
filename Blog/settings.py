"""
Django settings for Blog project.

Updated for deployment on Render.com with crash-prevention fixes.
"""

import os
from pathlib import Path
import dj_database_url  # Required for Render database connection

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================================================================
#  SECURITY SETTINGS
# ==============================================================================

# Get SECRET_KEY from environment. 
# Locally: Uses the fallback insecure key.
# Render: Uses the SECRET_KEY variable you set in the Dashboard.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-local-dev-key-change-me')

# DEBUG Logic:
# If the 'RENDER' environment variable exists, we turn DEBUG OFF.
# Otherwise (locally), it defaults to True.
DEBUG = 'RENDER' not in os.environ

# ALLOWED_HOSTS:
# Render provides the hostname in an environment variable automatically.
ALLOWED_HOSTS = []
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Add localhost for development and Render internal domains
ALLOWED_HOSTS.extend(['localhost', '127.0.0.1', '.onrender.com'])


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
    
    # Your Custom Apps (Ensure these match your actual folder names)
    'blog',
    'home', 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    
    # WhiteNoise is CRITICAL for Render. 
    # It allows the web server to serve CSS/Images directly.
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

# This automatically detects if we are on Render (using DATABASE_URL)
# or local (using db.sqlite3).

DATABASES = {
    'default': dj_database_url.config(
        # Use SQLite locally if DATABASE_URL is not found
        default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'),
        conn_max_age=600
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

# Where Docker/Render will collect files to (Must match your Dockerfile)
STATIC_ROOT = BASE_DIR / 'staticfiles'

# FIX: Prevent crash if 'static' folder is missing/empty
# We check if the folder exists before adding it to Django's search list.
STATICFILES_DIRS = []
if (BASE_DIR / 'static').exists():
    STATICFILES_DIRS.append(BASE_DIR / 'static')

# Enable WhiteNoise compression and caching support
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ==============================================================================
#  DEFAULT PRIMARY KEY FIELD TYPE
# ==============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'