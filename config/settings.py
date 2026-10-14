import importlib.util
import os
import platform
from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
env = environ.Env()
READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=True)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(BASE_DIR / ".env"))

env = environ.FileAwareEnv(
    DEBUG=(bool, False),
)

# GENERAL
# ------------------------------------------------------------------------------

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="django-insecure cin)v(4&89%_$17s0yezo=t+^1b*mq)=+348r-bv(ms#pm2y2#",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")
APPLICATION_REVISION = env("APPLICATION_REVISION", default="").strip()
APP_FQDN = env("APP_FQDN", default="localhost")

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["localhost"])
ALLOWED_HOSTS += [h for h in ("localhost", "127.0.0.1") if h not in ALLOWED_HOSTS]
CSRF_TRUSTED_ORIGINS = env.list(
    "DJANGO_CSRF_TRUSTED_ORIGINS", default=["http://localhost"]
)

# TLS terminates at the trusted public Gateway.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_SSL_REDIRECT = not DEBUG
SECURE_REDIRECT_EXEMPT = [r"^health/$"]
SECURE_HSTS_SECONDS = 0 if DEBUG else 3600
# The parent domain controls subdomain/preload policy; the site intentionally
# permits same-origin framing.
SILENCED_SYSTEM_CHECKS = ["security.W005", "security.W019", "security.W021"]

# Application definition

INSTALLED_APPS = [
    "daphne",
    "django_dbml",
    "admin_interface",
    "colorfield",
    "django.contrib.admin",
    "prose",
    "django.contrib.auth",
    "authuser",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "storages",
    "django_cleanup.apps.CleanupConfig",  # auto-delete files from FileField or ImageField if deleted in django-admin
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "taggit",
    "taggit_selectize",
    "tailwind",
    "theme",
    "import_export",
    "common",
    "denig",
    "essays",
    "footnotes",
    "imagekit",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

X_FRAME_OPTIONS = "SAMEORIGIN"

# DEBUG
# ------------------------------------------------------------------------------
# The production image installs no development dependencies.
DEBUG_TOOLBAR = DEBUG and importlib.util.find_spec("debug_toolbar") is not None
if DEBUG_TOOLBAR:
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
# -----------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": env("DB_HOST", default="localhost"),
        "PORT": env("DB_PORT", default="5432"),
        "NAME": env("DB_NAME", default="denig"),
        "USER": env("DB_USER", default="denig"),
        "PASSWORD": env("DB_PASS", default="password"),
        "CONN_MAX_AGE": 60,
        "CONN_HEALTH_CHECKS": True,
    }
}
if DB_LOCK_TIMEOUT := env("DB_LOCK_TIMEOUT", default=""):
    DATABASES["default"]["OPTIONS"] = {"options": f"-c lock_timeout={DB_LOCK_TIMEOUT}"}

AUTH_USER_MODEL = "authuser.User"

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/New_York"

USE_I18N = True
USE_TZ = True

# Theme
TAILWIND_APP_NAME = "theme"
INTERNAL_IPS = [
    "127.0.0.1",
]
if platform.system() == "Windows":
    NPM_BIN_PATH = "C:/Program Files/nodejs/npm.cmd"  # needed for windows

# Wagtail configuration
WAGTAILADMIN_BASE_URL = env(
    "WAGTAIL_BASE_URL",
    default=f"{'http' if DEBUG else 'https'}://{APP_FQDN}",
)
WAGTAIL_SITE_NAME = "Denig Scholarly Essays"
AWS_S3_FILE_OVERWRITE = False
WAGTAILIMAGES_RENDITION_STORAGE_OPTIONS = {"file_overwrite": False}
TAGGIT_TAGS_FROM_STRING = "taggit_selectize.utils.parse_tags"
TAGGIT_STRING_FROM_TAGS = "taggit_selectize.utils.join_tags"
SITE_ID = 1

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_URL = "/static/"
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Media files
MEDIA_URL = "/media/"
OBJ_STORAGE = env.bool("OBJ_STORAGE", default=False)
if OBJ_STORAGE:
    AWS_ACCESS_KEY_ID = env("OBJ_STORAGE_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = env("OBJ_STORAGE_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = env("OBJ_STORAGE_BUCKET_NAME")
    AWS_S3_ENDPOINT_URL = env("OBJ_STORAGE_ENDPOINT_URL")
    AWS_S3_REGION_NAME = env("OBJ_STORAGE_REGION", default=None)
    AWS_S3_ADDRESSING_STYLE = "path"
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_CUSTOM_DOMAIN = f"{APP_FQDN}/media"

    # The media-garage sidecar serves the public bucket at the app's /media/ URL.
    STORAGES["default"] = {
        "BACKEND": "storages.backends.s3.S3Storage",
    }
else:
    MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
