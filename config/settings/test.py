"""Settings for automated tests (SQLite in-memory, no Docker Postgres required)."""

import os

os.environ.setdefault("SECRET_KEY", "pytest-insecure-secret-key-not-for-production")

from .base import *

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "testserver"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
