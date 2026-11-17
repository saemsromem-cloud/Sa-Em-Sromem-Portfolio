"""Public pages: home, about, projects, skills, resume and contact."""

import sqlite3
import time

from flask import (
    Blueprint, abort, current_app, flash, redirect, render_template,
    request, send_from_directory, session, url_for,
)

from .. import content, db, forms
from ..security import csrf_protect

bp = Blueprint("public", __name__)

RESUME_FILE = "resume/Sa-Em-Sromem-Resume.pdf"
RESUME_DOWNLOAD_NAME = "Sa-Em-Sromem-Resume.pdf"


@bp.get("/")
def index():
    return render_template(
        "home.html",
        featured_projects=content.featured_projects(),
        featured_skills=content.FEATURED_SKILLS,
    )


@bp.get("/about")
def about():
    return render_template("about.html")


@bp.get("/projects")
def projects():
    return render_template("projects.html")


@bp.get("/projects/<slug>")
def project_detail(slug: str):
    project = content.get_project(slug)
    if project is None:
        abort(404)
    previous_project, next_project = content.neighbour_projects(slug)
    return render_template(
        "project_detail.html",
        project=project,
        previous_project=previous_project,
        next_project=next_project,
    )


@bp.get("/skills")
def skills():
    return render_template("skills.html")


@bp.get("/resume")
def resume():
    return render_template("resume.html")


@bp.get("/resume.pdf")
def resume_pdf():
    """The PDF opened in the browser."""
    return send_from_directory(current_app.static_folder, RESUME_FILE, mimetype="application/pdf")


@bp.get("/resume/download")
def resume_download():
    """The same PDF, saved to disk."""
    return send_from_directory(
        current_app.static_folder, RESUME_FILE,
        mimetype="application/pdf", as_attachment=True, download_name=RESUME_DOWNLOAD_NAME,
    )


# ------------------------------------------------------------------ Contact


def _render_contact(form: dict | None = None, errors: list[str] | None = None, status: int = 200):
    return render_template("contact.html", form=form or {}, errors=errors or []), status


def _redirect_to_contact_form():
    return redirect(url_for("public.contact", _anchor="form-status"))


@bp.route("/contact", methods=["GET", "POST"])
@csrf_protect
def contact():
    if request.method == "GET":
        session["contact_form_at"] = time.time()  # when the form was shown, for the speed check
        return _render_contact()

    # Hidden field that real visitors never fill in; bots often do.
    if request.form.get("website"):
        return _redirect_to_contact_form()

    form = forms.read_contact_form(request.form)
    errors = forms.validate_contact_form(form)
    if not errors:
        errors = forms.spam_problems(
            form, session.get("contact_form_at"), current_app.config["CONTACT_MIN_SECONDS"]
        )
    if errors:
        return _render_contact(form, errors, status=400)

    try:
        if db.recent_message_count(current_app.config["CONTACT_RECENT_MINUTES"]) >= current_app.config["CONTACT_RECENT_LIMIT"]:
            error = "Too many messages were sent recently. Please try again in a few minutes, or email me directly."
            return _render_contact(form, [error], status=429)
        if not db.message_exists(form):  # a double click should not store the message twice
            db.save_message(form)
    except sqlite3.Error:
        current_app.logger.exception("Could not save contact message")
        flash("Your message could not be saved. Please email me directly instead.", "error")
    else:
        session.pop("contact_form_at", None)
        flash("Thank you. Your message was sent, and I will reply by email.", "success")
    return _redirect_to_contact_form()
