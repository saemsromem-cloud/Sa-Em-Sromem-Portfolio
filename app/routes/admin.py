"""Private admin area: log in, then read and manage contact messages."""

import hmac
from functools import wraps

from flask import (
    Blueprint, current_app, flash, redirect, render_template, request, session, url_for,
)
from werkzeug.security import check_password_hash

from ..db import get_db
from ..security import csrf_protect

bp = Blueprint("admin", __name__)


@bp.after_request
def keep_out_of_search_engines(response):
    response.headers["X-Robots-Tag"] = "noindex, nofollow"
    return response


def admin_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin.login"))
        return view(*args, **kwargs)

    return wrapper


def credentials_are_valid(username: str, password: str) -> bool:
    expected_user = current_app.config["ADMIN_USERNAME"]
    password_hash = current_app.config["ADMIN_PASSWORD_HASH"]
    if not expected_user or not password_hash:
        return False  # admin login stays disabled until configured
    user_ok = hmac.compare_digest(username, expected_user)
    return check_password_hash(password_hash, password) and user_ok


@bp.route("/login", methods=["GET", "POST"])
@csrf_protect
def login():
    if session.get("admin_logged_in"):
        return redirect(url_for("admin.dashboard"))

    if request.method == "POST":
        if credentials_are_valid(request.form.get("username", "").strip(), request.form.get("password", "")):
            session.clear()
            session["admin_logged_in"] = True
            return redirect(url_for("admin.dashboard"))
        flash("Invalid username or password.", "error")

    return render_template("admin/login.html")


@bp.post("/logout")
@csrf_protect
def logout():
    session.clear()
    return redirect(url_for("admin.login"))


@bp.get("/dashboard")
@admin_required
def dashboard():
    db = get_db()
    messages = db.execute("SELECT * FROM messages ORDER BY id DESC").fetchall()
    unread = sum(1 for m in messages if m["status"] == "Unread")
    return render_template(
        "admin/dashboard.html",
        messages=messages,
        total_messages=len(messages),
        unread_messages=unread,
        read_messages=len(messages) - unread,
    )


@bp.post("/message/read/<int:message_id>")
@admin_required
@csrf_protect
def mark_as_read(message_id):
    db = get_db()
    db.execute("UPDATE messages SET status = 'Read' WHERE id = ?", (message_id,))
    db.commit()
    flash("Message marked as read.", "success")
    return redirect(url_for("admin.dashboard"))


@bp.post("/message/delete/<int:message_id>")
@admin_required
@csrf_protect
def delete_message(message_id):
    db = get_db()
    db.execute("DELETE FROM messages WHERE id = ?", (message_id,))
    db.commit()
    flash("Message deleted.", "success")
    return redirect(url_for("admin.dashboard"))
