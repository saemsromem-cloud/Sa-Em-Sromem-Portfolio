"""Small CSRF helper, so no extra dependency is needed."""

import hmac
import secrets
from functools import wraps

from flask import abort, request, session


def csrf_token() -> str:
    """Return this session's CSRF token, creating it on first use."""
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(16)
    return session["csrf_token"]


def csrf_protect(view):
    """Reject POST requests that do not carry the session's CSRF token."""

    @wraps(view)
    def wrapper(*args, **kwargs):
        if request.method == "POST":
            sent = request.form.get("csrf_token", "")
            expected = session.get("csrf_token", "")
            # An empty expected token means the session never loaded a form: reject.
            if not expected or not hmac.compare_digest(sent, expected):
                abort(400, description="Invalid or missing CSRF token.")
        return view(*args, **kwargs)

    return wrapper
