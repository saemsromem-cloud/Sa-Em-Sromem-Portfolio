"""Entry point for production servers: gunicorn wsgi:app"""

from dotenv import load_dotenv

load_dotenv()

from app import create_app  # noqa: E402  (must come after load_dotenv)

app = create_app()
