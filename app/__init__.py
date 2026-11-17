"""Application factory for the portfolio site."""

import os
from datetime import date
from pathlib import Path

from flask import Flask, render_template

from . import content, db
from .config import Config
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

    @app.context_processor
    def inject_site():
        return {"p": content.PROFILE, "site_url": app.config["SITE_URL"], "now_year": date.today().year}

    from .routes import admin, public

    app.register_blueprint(public.bp)
    app.register_blueprint(admin.bp)

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("error.html", code=404, message="That page does not exist."), 404

    @app.errorhandler(400)
    def bad_request(error):
        return render_template("error.html", code=400, message=error.description), 400

    @app.errorhandler(500)
    def server_error(_error):
        return render_template("error.html", code=500, message="Something went wrong on the server."), 500

    return app
