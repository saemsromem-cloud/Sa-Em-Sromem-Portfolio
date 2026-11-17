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


# ---------------------------------------------------------------- Messages


def save_message(form: dict) -> None:
    db = get_db()
    db.execute(
        "INSERT INTO messages (name, email, subject, message) VALUES (?, ?, ?, ?)",
        (form["name"], form["email"], form["subject"], form["message"]),
    )
    db.commit()


def message_exists(form: dict) -> bool:
    """True if the same person already sent this exact message (a double submit)."""
    row = get_db().execute(
        "SELECT 1 FROM messages WHERE email = ? AND subject = ? AND message = ? LIMIT 1",
        (form["email"], form["subject"], form["message"]),
    ).fetchone()
    return row is not None


def recent_message_count(minutes: int) -> int:
    """How many messages arrived in the last few minutes (all senders)."""
    row = get_db().execute(
        "SELECT COUNT(*) FROM messages WHERE created_at >= datetime('now', ?)",
        (f"-{int(minutes)} minutes",),
    ).fetchone()
    return row[0]
