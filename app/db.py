"""SQLite access for contact messages."""

import sqlite3
from pathlib import Path

from flask import current_app, g

SCHEMA = """
CREATE TABLE IF NOT EXISTS messages (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT NOT NULL,
    email      TEXT NOT NULL,
    subject    TEXT NOT NULL,
    message    TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status     TEXT NOT NULL DEFAULT 'Unread' CHECK (status IN ('Unread', 'Read'))
)
"""


def get_db() -> sqlite3.Connection:
    """Return one connection per request, with rows accessible by column name."""
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE_PATH"])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(_error=None) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
    Path(current_app.config["DATABASE_PATH"]).parent.mkdir(parents=True, exist_ok=True)
    db = get_db()
    db.execute(SCHEMA)
    db.commit()
