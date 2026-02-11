from pathlib import Path
import os

import dj_database_url
from django.core.exceptions import ImproperlyConfigured
import environ

# set casting, default value
env = environ.Env(
    DEBUG=(bool, False),
    DB_SSL_REQUIRE=(bool, True),
    DB_CONN_MAX_AGE=(int, 600),
)

BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file (lokaal / als aanwezig)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# False if not in os.environ because of casting above
DEBUG = env.bool('DEBUG', default=False)

# CSRF trusted origins (space-separated in env)
CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', '').split()

# -----------------------
# Database configuration
# -----------------------
DATABASE_URL = env('DATABASE_URL', default=None)

if DATABASE_URL:
    # Postgres via DATABASE_URL
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=env.int('DB_CONN_MAX_AGE', default=600),
            ssl_require=env.bool('DB_SSL_REQUIRE', default=True),
        )
    }
else:
    # Lokale development fallback
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Hard fail in production als DATABASE_URL ontbreekt
if not DEBUG and not DATABASE_URL:
    raise ImproperlyConfigured('DATABASE_URL is not set (required in production).')

# -----------------------
# Basic security / hosts
# -----------------------
ALLOWED_HOSTS = [h.strip() for h in env.str('ALLOWED_HOSTS', default='').split(',') if h.strip()]
SECRET_KEY = env('SECRET_KEY')

CAPTCHA_FAILURE_FORM = True

# Application definition
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'accounts.apps.AccountsConfig',

    'about',
    'agenda',
    'contact',
    'liederen',
    'planning',
    'public_content',
    'sponsors',
    'website',

    'captcha',

    'crispy_forms',
    'crispy_bootstrap5',

    'storages',
]
INSTALLED_APPS += ["django_cleanup.apps.CleanupConfig"]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'accounts.middleware.ForcePasswordChangeMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

JAZZMIN_SETTINGS = {
    'site_title': 'Krakend Tuig Admin',
    'site_header': 'Krakend Tuig',
    'site_brand': 'Krakend Tuig',
    'welcome_sign': 'Welkom in de beheeromgeving van Krakend Tuig',
    'copyright': 'Krakend Tuig',
    'topmenu_links': [
        {'name': 'Website', 'url': '/', 'new_window': True},
    ],
    'show_sidebar': True,
    'navigation_expanded': True,
    'search_model': [
        'auth.User',
    ],
}

JAZZMIN_SETTINGS['custom_css'] = 'css/admin.css'

JAZZMIN_UI_TWEAKS = {
    'theme': 'simplex',
    'dark_mode_theme': 'darkly',
    'navbar_small_text': False,
    'footer_small_text': True,
    'body_small_text': False,
    'brand_small_text': False,
    'sidebar_nav_small_text': False,
    'sidebar_disable_expand': False,
    'sidebar_nav_child_indent': True,
    'navbar': 'navbar-dark navbar-navy',
    'accent': 'accent-navy',
    'sidebar': 'sidebar-dark-navy',
    'button_classes': {
        'primary': 'btn-primary',
        'secondary': 'btn-secondary',
        'info': 'btn-info',
        'warning': 'btn-warning',
        'danger': 'btn-danger',
        'success': 'btn-success',
    },
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'nl'
TIME_ZONE = 'Europe/Amsterdam'
USE_I18N = True
USE_TZ = True

# -----------------------
# Static & Media
# -----------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

USE_S3 = os.environ.get('USE_S3', '0') == '1'

# Default storages (lokaal)
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
WHITENOISE_KEEP_ONLY_HASHED_FILES = False

# S3 settings (alleen als USE_S3=1)
if USE_S3:
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', 'krakendtuig-media')
    AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'eu-north-1')

    AWS_DEFAULT_ACL = None
    AWS_QUERYSTRING_AUTH = False

    # Optioneel: caching headers voor S3 objecten (kan later strakker)
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }

    # Alleen MEDIA naar S3 (static blijft via WhiteNoise)
    STORAGES["default"] = {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    }

    MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com/'


# -----------------------
# SMTP Configuration
# -----------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

DEFAULT_FROM_EMAIL = env.str('GMAIL_FROM_EMAIL', default='')
EMAIL_HOST_USER = DEFAULT_FROM_EMAIL
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASS', default='')

CONTACT_RECIPIENT_EMAIL = env.str('CONTACT_RECIPIENT_EMAIL', default=EMAIL_HOST_USER)

# -----------------------
# Authentication & Sessions
# -----------------------
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'home'

SESSION_COOKIE_AGE = 60 * 60 * 24 * 365
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    USE_X_FORWARDED_HOST = True

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
