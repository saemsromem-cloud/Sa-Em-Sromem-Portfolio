"""Configuration, read from environment variables (see .env.example)."""

import os


def _flag(name: str, default: bool = False) -> bool:
    return os.environ.get(name, str(default)).strip().lower() in {"1", "true", "yes"}


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DATABASE_PATH = os.environ.get("DATABASE_PATH")  # defaults to instance/messages.db
    SITE_URL = os.environ.get("SITE_URL", "http://127.0.0.1:5000").rstrip("/")
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "")
    ADMIN_PASSWORD_HASH = os.environ.get("ADMIN_PASSWORD_HASH", "")

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = _flag("SESSION_COOKIE_SECURE")
    MAX_CONTENT_LENGTH = 32 * 1024  # contact form posts are tiny; reject anything bigger
