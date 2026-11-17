"""Application factory for the portfolio site."""

import os
from datetime import date
from pathlib import Path

from flask import Flask, render_template, request, url_for

from . import content, db
from .config import Config
from .navigation import build_nav
from .security import csrf_token


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    if not app.config["DATABASE_PATH"]:
        app.config["DATABASE_PATH"] = str(Path(app.instance_path) / "messages.db")

    if not app.config["SECRET_KEY"]:
        if os.environ.get("FLASK_DEBUG") == "1" or app.testing:
            app.config["SECRET_KEY"] = "dev-only-secret"  # local development only
        else:
            raise RuntimeError("SECRET_KEY is not set. Copy .env.example to .env and fill it in.")

    app.teardown_appcontext(db.close_db)
    with app.app_context():
        db.init_db()

    app.jinja_env.globals["csrf_token"] = csrf_token

    def static_url(filename: str) -> str:
        """Static file URL with the file's modified time, so a changed file is never served stale."""
        try:
            version = int((Path(app.static_folder) / filename).stat().st_mtime)
        except OSError:
            return url_for("static", filename=filename)
        return url_for("static", filename=filename, v=version)

    app.jinja_env.globals["static_url"] = static_url

    @app.context_processor
    def inject_site():
        return {
            "p": content.PROFILE,
            "c": content,
            "site_url": app.config["SITE_URL"],
            "now_year": date.today().year,
            "nav_items": build_nav(request.endpoint),
        }

    from .routes import admin, public, seo

    app.register_blueprint(public.bp)
    app.register_blueprint(seo.bp)
    app.register_blueprint(admin.bp)

    @app.after_request
    def set_security_headers(response):
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        response.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        return response

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("error.html", code=404, message="That page does not exist."), 404

    @app.errorhandler(405)
    def method_not_allowed(_error):
        return render_template("error.html", code=405, message="That action is not allowed on this page."), 405

    @app.errorhandler(400)
    def bad_request(error):
        return render_template("error.html", code=400, message=error.description), 400

    @app.errorhandler(413)
    def too_large(_error):
        return render_template("error.html", code=413, message="That request was too large."), 413

    @app.errorhandler(500)
    def server_error(_error):
        return render_template("error.html", code=500, message="Something went wrong on the server."), 500

    return app
