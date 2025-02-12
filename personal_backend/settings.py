"""
Django settings for personal_backend project.

This file is organized into logical sections:
1. Core Django Settings
2. Database Configuration
3. Security Settings
4. Authentication & Authorization
5. API & DRF Settings
6. CORS & CSRF Configuration
7. Cache & Sessions
8. File Handling
9. Email Settings
10. Channels & WebSocket
11. Logging & Monitoring
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

###################
# CORE SETTINGS   #
###################

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

#########################
# DOMAIN SETTINGS       #
#########################

# Add this new section for domain configuration
DOMAIN = os.getenv('DOMAIN', 'd9042n.tech')
ADMIN_DOMAIN = f'admin.personal.{DOMAIN}'
API_DOMAIN = f'api.personal.{DOMAIN}'

# Update ALLOWED_HOSTS to use domain variables
ALLOWED_HOSTS = [
    ADMIN_DOMAIN,
    API_DOMAIN,
    'localhost',
    '127.0.0.1',
]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third party apps
    "rest_framework",
    "corsheaders",
    "channels",
    "drf_yasg",

    # Local apps
    'users',
    'notifications',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",  # Security middleware first
    "corsheaders.middleware.CorsMiddleware",  # CORS before CommonMiddleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "personal_backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

#########################
# DATABASE SETTINGS     #
#########################

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

#########################
# SECURITY SETTINGS     #
#########################

# SSL/HTTPS Settings
SECURE_SSL_REDIRECT = not DEBUG
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Security Headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'SAMEORIGIN'  # Changed from 'DENY' to allow admin site to work

# HSTS Settings
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Referrer Policy - Updated for admin compatibility
SECURE_REFERRER_POLICY = 'same-origin'

#################################
# AUTHENTICATION & PERMISSIONS  #
#################################

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 10,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# API Authentication
API_REQUIRE_AUTH = os.getenv('API_REQUIRE_AUTH', 'True').lower() == 'true'

#########################
# API & DRF SETTINGS    #
#########################

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated' if API_REQUIRE_AUTH
        else 'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    }
}

#########################
# CORS CONFIGURATION    #
#########################

CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000').split(',')
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ['DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT']
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
CORS_EXPOSE_HEADERS = ['content-type', 'x-csrftoken']
CORS_PREFLIGHT_MAX_AGE = 86400  # 24 hours

if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True

#########################
# CSRF CONFIGURATION    #
#########################

CSRF_COOKIE_DOMAIN = f'.personal.{DOMAIN}'  # Allow sharing between subdomains
CSRF_TRUSTED_ORIGINS = [
    f'https://{ADMIN_DOMAIN}',
    f'https://{API_DOMAIN}',
    f'https://{DOMAIN}',
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]
CSRF_COOKIE_NAME = '__Secure-csrftoken' if not DEBUG else 'csrftoken'
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SECURE = not DEBUG
CSRF_USE_SESSIONS = True
CSRF_COOKIE_HTTPONLY = False  # Changed to False for admin site compatibility

#########################
# SESSION SETTINGS      #
#########################

SESSION_COOKIE_DOMAIN = f'.personal.{DOMAIN}'  # Match CSRF domain
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_NAME = '__Secure-sessionid' if not DEBUG else 'sessionid'
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_HTTPONLY = True

#########################
# FILE HANDLING         #
#########################

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

#########################
# INTERNATIONALIZATION  #
#########################

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

#########################
# CHANNELS & WEBSOCKET  #
#########################

ASGI_APPLICATION = 'personal_backend.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(os.getenv('REDIS_HOST', 'redis'), 6379)],
        },
    },
}

#########################
# EMAIL SETTINGS        #
#########################

ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True

#########################
# MISC SETTINGS         #
#########################

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
