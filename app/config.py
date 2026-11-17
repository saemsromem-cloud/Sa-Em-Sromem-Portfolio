"""Configuration, read from environment variables (see .env.example)."""

import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env", override=True)


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

    # Static files carry a ?v=<file time> parameter, so browsers can cache them for a week.
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(days=7)

    # Contact form spam protection.
    CONTACT_MIN_SECONDS = float(os.environ.get("CONTACT_MIN_SECONDS", "3"))  # fastest a person can submit
    CONTACT_RECENT_LIMIT = int(os.environ.get("CONTACT_RECENT_LIMIT", "10"))  # messages allowed...
    CONTACT_RECENT_MINUTES = int(os.environ.get("CONTACT_RECENT_MINUTES", "10"))  # ...per this window