"""Contact form: reading, validation and basic spam checks.

Kept separate from the routes so the rules can be read (and tested) on their own.
"""

import re
import time

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]{2,}$")
LINK_PATTERN = re.compile(r"https?://|www\.", re.IGNORECASE)

LIMITS = {"name": 100, "email": 254, "subject": 150, "message": 3000}
MINIMUMS = {"name": 2, "subject": 3, "message": 10}
SINGLE_LINE_FIELDS = ("name", "email", "subject")
MAX_LINKS_IN_MESSAGE = 2

FIELD_LABELS = {"name": "Name", "email": "Email", "subject": "Subject", "message": "Message"}


def read_contact_form(source) -> dict:
    """Pick the four expected fields from request.form and trim them."""
    return {field: (source.get(field) or "").strip() for field in LIMITS}


def validate_contact_form(form: dict) -> list[str]:
    """Return a list of problems with the submitted form (empty if valid)."""
    errors = []
    for field, minimum in MINIMUMS.items():
        if len(form[field]) < minimum:
            errors.append(f"{FIELD_LABELS[field]} must contain at least {minimum} characters.")
    if not EMAIL_PATTERN.match(form["email"]):
        errors.append("Enter a valid email address.")
    for field, limit in LIMITS.items():
        if len(form[field]) > limit:
            errors.append(f"{FIELD_LABELS[field]} must be {limit} characters or fewer.")
    if any(char in form[field] for field in SINGLE_LINE_FIELDS for char in "\r\n"):
        errors.append("Name, email and subject must be on a single line.")
    return errors


def spam_problems(form: dict, started_at: float | None, min_seconds: float) -> list[str]:
    """Checks that catch most automated submissions without a CAPTCHA.

    The hidden honeypot field is checked in the route, before validation.
    """
    problems = []
    if len(LINK_PATTERN.findall(form["message"])) > MAX_LINKS_IN_MESSAGE:
        problems.append("Please remove some of the links from your message.")
    # A person needs a few seconds to fill the form in; a script does not.
    if started_at is None or time.time() - started_at < min_seconds:
        problems.append("That was sent too quickly. Please check your message and send it again.")
    return problems
