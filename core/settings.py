"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# گرفتن نسخه برنامه از .env
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")  # نسخه پیش‌فرض 1.0.0
FIX_PASSWORD = os.getenv("FIX_PASSWORD", "FixedPassword123")
ORG_NAME = os.getenv("ORG_NAME", "محل قرار گرفتن نام سازمان")
ORG_WEBSITE = os.getenv("ORG_WEBSITE", "#")
SMS_NUMBER = os.getenv("SMS_NUMBER", " ")
WEBSERVER_IP = os.getenv("WEBSERVER_IP", "127.0.0.1")
LEAST_CREDIT = os.getenv("LEAST_CREDIT", "500000")
MELLI_PAYAMAK_API_KEY = os.getenv("MELLI_PAYAMAK_API_KEY", "abc")
LEAST_CREDIT_NUM = os.getenv("LEAST_CREDIT_NUM", "20")
PANEL_WEB_ADDRESS = os.getenv("PANEL_WEB_ADDRESS", "#")
PANEL_NAME = os.getenv("PANEL_NAME", "---")
EMAIL_DOMAIN = os.getenv("EMAIL_DOMAIN", "automail.fums.ac.ir")
FORTIGATE_API_KEY = os.getenv("FORTIGATE_API_KEY", "")
FORTIGATE_IP = os.getenv("FORTIGATE_IP", "")
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-5&ajgrnic0b3n=&(1(bj7kaqum_++l9!uv*0js1w&vk3el_1)h"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG =os.environ.get('DEBUG', 'False').lower() in ['true', '1', 't', 'yes']

ALLOWED_HOSTS = [WEBSERVER_IP]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "usrsmgmnt",
    "django_recaptcha",
    #'django_db_logger',
    "django_jalali",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "usrsmgmnt.middleware.RequestMiddleware",
]

ROOT_URLCONF = "core.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
            os.path.join(BASE_DIR, "usrsmgmnt/templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "usrsmgmnt.context_processors.app_version",
                "usrsmgmnt.context_processors.current_path",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

if DEBUG:
    DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
else:
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DATABASE-NAME', 'postgres'),
        'USER': os.getenv('DATABASE-USER', 'postgres'),
        'PASSWORD': os.getenv('DATABASE-PASSWORD', 'postgres'),
        'HOST': os.getenv('DATABASE-HOST', 'localhost'),
        'PORT': os.getenv('DATABASE-PORT', 5432),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/


STATIC_URL = "static/"
MEDIA_URL = "media/"
STATIC_ROOT =   os.path.join(BASE_DIR, "static")

# Directory to hold your static files
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static"),
# ]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "usrsmgmnt.LinFortiUsers"
LANGUAGE_CODE = "fa"
TIME_ZONE = "Asia/Tehran"
USE_I18N = True
USE_L10N = True
USE_TZ = True
# settings.py
# settings.py
RECAPTCHA_PUBLIC_KEY = "6LcmOGUqAAAAAGh431eYmoup5IFHvUipgHwX6pEX"
RECAPTCHA_PRIVATE_KEY = "6LcmOGUqAAAAAOfVCD8LL335UH2_aoMaTilD09q8"

#'%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "%(levelname)s--%(module)s-- %(message)s"},
        "simple": {"format": "%(levelname)s %(asctime)s %(message)s"},
    },
    "handlers": {
        "db_handler": {
            "level": "DEBUG",
            "class": "usrsmgmnt.handlers.DatabaseLogHandler",
            "formatter": "verbose",
        }
    },
    "loggers": {"db": {"handlers": ["db_handler"], "level": "DEBUG"}},
}

DJANGO_DB_LOGGER_ENABLE_FORMATTER = True
DJANGO_DB_LOGGER_ADMIN_LIST_PER_PAGE = int(
    os.getenv("DJANGO_DB_LOGGER_ADMIN_LIST_PER_PAGE", 30)
)
# CSRF_TRUSTED_ORIGINS=['http://192.168.110.149:8000']
