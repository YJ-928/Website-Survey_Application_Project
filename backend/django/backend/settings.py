import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

# --------------------------------------------------
# Base
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# --------------------------------------------------
# Core
# --------------------------------------------------
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
DEBUG = os.getenv("DEBUG") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

# --------------------------------------------------
# Installed Apps
# --------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_yasg",

    # Local
    "api",
]

# --------------------------------------------------
# Middleware
# --------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# --------------------------------------------------
# CORS / CSRF
# --------------------------------------------------
CORS_ALLOW_ALL_ORIGINS = os.getenv("CORS_ALLOW_ALL_ORIGINS") == "True"

CORS_ALLOWED_ORIGINS = os.getenv(
    "CORS_ALLOWED_ORIGINS", ""
).split(",")

CSRF_TRUSTED_ORIGINS = os.getenv(
    "CSRF_TRUSTED_ORIGINS", ""
).split(",")

CORS_ALLOW_CREDENTIALS = True

# --------------------------------------------------
# URLs / WSGI
# --------------------------------------------------
ROOT_URLCONF = "backend.urls"
WSGI_APPLICATION = "backend.wsgi.application"

# --------------------------------------------------
# Templates
# --------------------------------------------------
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

# --------------------------------------------------
# Database (SQLite – POC)
# --------------------------------------------------
DATABASES = {
    "default": {
      "ENGINE": "django.db.backends.sqlite3",
      "NAME": BASE_DIR / "db.sqlite3",
        # "ENGINE": os.getenv("DB_ENGINE"),
        # "NAME":os.getenv("DB_NAME"),
        # "USER":os.getenv("DB_USER"),
        # "PASSWORD":os.getenv("DB_PASSWORD"),
        # "HOST":os.getenv("DB_HOST"),
        # "PORT":os.getenv("DB_PORT")
    }
}

# --------------------------------------------------
# Password Validation
# --------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --------------------------------------------------
# I18N
# --------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --------------------------------------------------
# Static
# --------------------------------------------------

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"

# --------------------------------------------------
# JWT Keys (RS256)
# --------------------------------------------------
JWT_PRIVATE_KEY_PATH = BASE_DIR / os.getenv("JWT_PRIVATE_KEY_PATH")
JWT_PUBLIC_KEY_PATH = BASE_DIR / os.getenv("JWT_PUBLIC_KEY_PATH")

with open(JWT_PRIVATE_KEY_PATH, "r", encoding="utf-8") as f:
    JWT_PRIVATE_KEY = f.read()

with open(JWT_PUBLIC_KEY_PATH, "r", encoding="utf-8") as f:
    JWT_PUBLIC_KEY = f.read()

# --------------------------------------------------
# Django REST Framework
# --------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_THROTTLE_CLASSES": (
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ),
    "DEFAULT_THROTTLE_RATES": {
        "anon": os.getenv("ANON_RATE_LIMIT", "50/minute"),
        "user": os.getenv("USER_RATE_LIMIT", "100/minute"),
    },
}

# --------------------------------------------------
# SIMPLE JWT (Bearer + RS256)
# --------------------------------------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=int(os.getenv("JWT_ACCESS_TOKEN_LIFETIME_MINUTES", 60))
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        minutes=int(os.getenv("JWT_REFRESH_TOKEN_LIFETIME_MINUTES", 7))
    ),
    "ROTATE_REFRESH_TOKENS": os.getenv("JWT_ROTATE_REFRESH_TOKENS") == "True",
    "BLACKLIST_AFTER_ROTATION": os.getenv(
        "JWT_REFRESH_BLACKLIST_AFTER_ROTATION"
    ) == "True",
    "ALGORITHM": "RS256",
    "SIGNING_KEY": JWT_PRIVATE_KEY,
    "VERIFYING_KEY": JWT_PUBLIC_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "UPDATE_LAST_LOGIN": True,
}

# --------------------------------------------------
# Swagger
# --------------------------------------------------
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Bearer <access_token>",
        }
    },
    "USE_SESSION_AUTH": False,
}

# --------------------------------------------------
# RSA Encryption / Decryption Keys
# --------------------------------------------------
ENCRYPTION_PRIVATE_KEY_PATH = BASE_DIR / os.getenv(
    "ENCRYPTION_PRIVATE_KEY_PATH"
)
ENCRYPTION_PUBLIC_KEY_PATH = BASE_DIR / os.getenv(
    "ENCRYPTION_PUBLIC_KEY_PATH"
)

with open(ENCRYPTION_PRIVATE_KEY_PATH, "r", encoding="utf-8") as f:
    ENCRYPTION_PRIVATE_KEY = f.read()

with open(ENCRYPTION_PUBLIC_KEY_PATH, "r", encoding="utf-8") as f:
    ENCRYPTION_PUBLIC_KEY = f.read()

# --------------------------------------------------
# Super Admin Credentials
# --------------------------------------------------
DEFAULT_SUPER_ADMIN_EMAIL = os.getenv("DEFAULT_SUPER_ADMIN_EMAIL")
DEFAULT_SUPER_ADMIN_PASSWORD = os.getenv("DEFAULT_SUPER_ADMIN_PASSWORD")
DEFAULT_SUPER_ADMIN_NAME = os.getenv("DEFAULT_SUPER_ADMIN_NAME")
DEFAULT_SUPER_ADMIN_MOBILE = os.getenv("DEFAULT_SUPER_ADMIN_MOBILE")
DEFAULT_SUPER_ADMIN_LOCATION = os.getenv("DEFAULT_SUPER_ADMIN_LOCATION")

# --------------------------------------------------
# Frontend URLs
# --------------------------------------------------
FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL")
FRONTEND_INVITE_PATH = os.getenv("FRONTEND_INVITE_PATH")

# --------------------------------------------------
# Email Configuration (SMTP)
# --------------------------------------------------
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND")

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS") == "True"

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

DEFAULT_FROM_EMAIL = os.getenv(
    "DEFAULT_FROM_EMAIL",
    EMAIL_HOST_USER,
)

# --------------------------------------------------
# Logging Configuration
# --------------------------------------------------
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} [{name}] {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs/backend.log",
            "formatter": "verbose",
        },
    },

    "root": {
        "handlers": ["console", "file"],
        "level": "INFO",
    },
}

# Warning Fix
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Seed Nalgonda Disctrict Data
SEED_DATA = os.getenv("SEED_DATA", "False").lower() == "true"
