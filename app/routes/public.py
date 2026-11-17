"""Public pages: the portfolio, contact form, resume download and SEO files."""

import re
import sqlite3

from flask import (
    Blueprint, Response, current_app, flash, redirect, render_template,
    request, send_from_directory, url_for,
)

from .. import content
from ..db import get_db
from ..security import csrf_protect

bp = Blueprint("public", __name__)

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
LIMITS = {"name": 100, "email": 254, "subject": 150, "message": 3000}

# The old multi-page site used these URLs; keep them working.
LEGACY_REDIRECTS = {
    "/pages/about": "about", "/pages/about.html": "about", "/about": "about",
    "/pages/projects": "projects", "/pages/projects.html": "projects", "/projects": "projects",
    "/pages/contact": "contact", "/pages/contact.html": "contact",
    "/index.html": "top",
}


def validate_contact_form(form: dict) -> list[str]:
    """Return a list of problems with the submitted form (empty if valid)."""
    errors = []
    if len(form["name"]) < 2:
        errors.append("Name must contain at least 2 characters.")
    if not EMAIL_PATTERN.match(form["email"]):
        errors.append("Enter a valid email address.")
    if len(form["subject"]) < 3:
        errors.append("Subject must contain at least 3 characters.")
    if len(form["message"]) < 10:
        errors.append("Message must contain at least 10 characters.")
    for field, limit in LIMITS.items():
        if len(form[field]) > limit:
            errors.append(f"{field.capitalize()} must be {limit} characters or fewer.")
    return errors


@bp.get("/")
def index():
    return render_template("index.html", c=content)


@bp.post("/contact")
@csrf_protect
def contact():
    # Hidden field that real visitors never fill in; bots often do.
    if request.form.get("website"):
        return redirect(url_for("public.index", _anchor="contact"))

    form = {key: request.form.get(key, "").strip() for key in LIMITS}
    errors = validate_contact_form(form)
    if errors:
        return render_template("index.html", c=content, errors=errors, form=form), 400

    try:
        db = get_db()
        db.execute(
            "INSERT INTO messages (name, email, subject, message) VALUES (?, ?, ?, ?)",
            (form["name"], form["email"], form["subject"], form["message"]),
        )
        db.commit()
    except sqlite3.Error:
        current_app.logger.exception("Could not save contact message")
        flash("Your message could not be saved. Please email me directly instead.", "error")
    else:
        flash("Thanks, your message was sent. I will reply by email.", "success")
    return redirect(url_for("public.index", _anchor="contact"))


@bp.get("/resume")
def resume():
    return send_from_directory(
        current_app.static_folder, "resume/Sa-Em-Sromem-Resume.pdf", mimetype="application/pdf"
    )


@bp.get("/robots.txt")
def robots():
    site = current_app.config["SITE_URL"]
    body = f"User-agent: *\nAllow: /\nDisallow: /login\nDisallow: /dashboard\n\nSitemap: {site}/sitemap.xml\n"
    return Response(body, mimetype="text/plain")


@bp.get("/sitemap.xml")
def sitemap():
    site = current_app.config["SITE_URL"]
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"  <url><loc>{site}/</loc><priority>1.0</priority></url>\n"
        f"  <url><loc>{site}/resume</loc><priority>0.6</priority></url>\n"
        "</urlset>\n"
    )
    return Response(xml, mimetype="application/xml")


@bp.get("/google9e1b677973c92115.html")
def google_site_verification():
    """Keeps the existing Google Search Console verification working."""
    return Response(
        "google-site-verification: google9e1b677973c92115.html", mimetype="text/html"
    )


@bp.get("/favicon.ico")
def favicon():
    return redirect(url_for("static", filename="favicon.svg"), code=301)


def _legacy_redirect(anchor: str):
    return redirect(url_for("public.index", _anchor="" if anchor == "top" else anchor), code=301)


for _path, _anchor in LEGACY_REDIRECTS.items():
    bp.add_url_rule(
        _path, endpoint=f"legacy_{_path.strip('/').replace('/', '_').replace('.', '_')}",
        view_func=lambda anchor=_anchor: _legacy_redirect(anchor),
    )
bp.add_url_rule("/pages/resume", endpoint="legacy_resume", view_func=lambda: redirect(url_for("public.resume"), code=301))
bp.add_url_rule("/pages/resume.html", endpoint="legacy_resume_html", view_func=lambda: redirect(url_for("public.resume"), code=301))
