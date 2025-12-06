from pathlib import Path
from decouple import config  # ✅ REQUIRED to use `config`
import os

# ---------------------------
# Base directories
# ---------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / 'Cyberbot' / 'templates'

# ---------------------------
# Load sensitive values from .env
# ---------------------------
SECRET_KEY = config('SECRET_KEY')
DEBUG = True  # Set False for production
GOOGLE_SAFE_BROWSING_API_KEY = config('GOOGLE_SAFE_BROWSING_API_KEY')

ALLOWED_HOSTS = ["*"]  # You can restrict this in production

# ---------------------------
# Installed apps
# ---------------------------
INSTALLED_APPS = [
    'corsheaders',  # ✅ must be at top
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Cyberbot',
]

# ---------------------------
# Middleware
# ---------------------------
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # ✅ must be first
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ---------------------------
# URLs & Templates
# ---------------------------
ROOT_URLCONF = 'CYBERBOTDJANGO2.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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

WSGI_APPLICATION = 'CYBERBOTDJANGO2.wsgi.application'

# ---------------------------
# Database
# ---------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ---------------------------
# Password validators
# ---------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------------------
# Internationalization
# ---------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Dhaka'
USE_I18N = True
USE_TZ = True

# ---------------------------
# Static files
# ---------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# ---------------------------
# Media files
# ---------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ---------------------------
# Custom user model
# ---------------------------
AUTH_USER_MODEL = 'Cyberbot.CustomUser'

# ---------------------------
# External API URLs
# ---------------------------
HIBP_API_URL = 'https://api.pwnedpasswords.com/range/'
SAFE_BROWSING_API_URL = 'https://safebrowsing.googleapis.com/v4/threatMatches:find'

# ---------------------------
# Default primary key field type
# ---------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------------------
# CORS Settings
# ---------------------------
# For testing: allow all origins
CORS_ALLOW_ALL_ORIGINS = True

# For production: allow only specific frontend domains
# CORS_ALLOWED_ORIGINS = [
#     "http://127.0.0.1:8000",
#     "https://yourfrontenddomain.com",
# ]
