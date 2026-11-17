import re

import pytest
from werkzeug.security import generate_password_hash

from app import create_app


@pytest.fixture()
def app(tmp_path):
    return create_app({
        "TESTING": True,
        "SECRET_KEY": "test-secret",
        "DATABASE_PATH": str(tmp_path / "test.db"),
        "SITE_URL": "https://example.test",
        "ADMIN_USERNAME": "owner",
        "ADMIN_PASSWORD_HASH": generate_password_hash("correct horse battery"),
    })


@pytest.fixture()
def client(app):
    return app.test_client()


def token(client, path="/"):
    html = client.get(path).get_data(as_text=True)
    return re.search(r'name="csrf_token" value="([0-9a-f]+)"', html).group(1)


VALID = {"name": "Dara", "email": "dara@example.com", "subject": "Internship", "message": "We would like to talk."}


def test_home_has_required_content(client):
    html = client.get("/").get_data(as_text=True)
    for text in ["Aspiring Backend Developer", "Download resume", "View projects",
                 'id="about"', 'id="skills"', 'id="projects"', 'id="education"',
                 'id="learning"', 'id="contact"', "REST API", "Passerelles"]:
        assert text in html
    assert "<title>" in html and 'rel="canonical"' in html and 'property="og:image"' in html


def test_phone_number_not_on_website(client):
    assert "9335" not in client.get("/").get_data(as_text=True)


def test_resume_download_is_a_pdf(client):
    r = client.get("/resume")
    assert r.status_code == 200 and r.mimetype == "application/pdf" and r.data.startswith(b"%PDF")


def test_seo_files(client):
    assert "https://example.test/sitemap.xml" in client.get("/robots.txt").get_data(as_text=True)
    assert "<loc>https://example.test/</loc>" in client.get("/sitemap.xml").get_data(as_text=True)
    assert client.get("/google9e1b677973c92115.html").status_code == 200


def test_legacy_urls_redirect(client):
    r = client.get("/pages/projects.html")
    assert r.status_code == 301 and r.headers["Location"].endswith("/#projects")
    assert client.get("/pages/resume").headers["Location"].endswith("/resume")


def test_contact_saves_message(client, app):
    r = client.post("/contact", data={**VALID, "csrf_token": token(client)})
    assert r.status_code == 302
    with app.app_context():
        from app.db import get_db
        rows = get_db().execute("SELECT * FROM messages").fetchall()
    assert len(rows) == 1 and rows[0]["status"] == "Unread"


def test_contact_rejects_invalid_input(client):
    r = client.post("/contact", data={**VALID, "email": "nope", "csrf_token": token(client)})
    assert r.status_code == 400 and "valid email" in r.get_data(as_text=True)


def test_contact_requires_csrf_token(client):
    assert client.post("/contact", data=VALID).status_code == 400


def test_contact_honeypot_discards_bots(client, app):
    client.post("/contact", data={**VALID, "website": "http://spam", "csrf_token": token(client)})
    with app.app_context():
        from app.db import get_db
        assert get_db().execute("SELECT COUNT(*) FROM messages").fetchone()[0] == 0


def test_sql_injection_text_is_stored_as_plain_text(client, app):
    payload = "x'); DROP TABLE messages;--"
    client.post("/contact", data={**VALID, "subject": payload, "csrf_token": token(client)})
    with app.app_context():
        from app.db import get_db
        assert get_db().execute("SELECT subject FROM messages").fetchone()[0] == payload


def login(client, password="correct horse battery"):
    return client.post("/login", data={"username": "owner", "password": password, "csrf_token": token(client, "/login")})


def test_dashboard_requires_login(client):
    r = client.get("/dashboard")
    assert r.status_code == 302 and "/login" in r.headers["Location"]


def test_wrong_password_rejected(client):
    assert login(client, "wrong").status_code == 200
    assert client.get("/dashboard").status_code == 302


def test_admin_flow(client, app):
    client.post("/contact", data={**VALID, "csrf_token": token(client)})
    assert login(client).status_code == 302
    page = client.get("/dashboard")
    assert page.status_code == 200 and "Dara" in page.get_data(as_text=True)
    assert page.headers["X-Robots-Tag"] == "noindex, nofollow"
    t = token(client, "/dashboard")
    assert client.post("/message/read/1", data={"csrf_token": t}).status_code == 302
    assert client.post("/message/delete/1", data={"csrf_token": t}).status_code == 302
    with app.app_context():
        from app.db import get_db
        assert get_db().execute("SELECT COUNT(*) FROM messages").fetchone()[0] == 0


def test_admin_actions_need_csrf_and_login(client):
    assert client.post("/message/delete/1", data={}).status_code == 302  # not logged in
    login(client)
    assert client.post("/message/delete/1", data={}).status_code == 400  # no token


def test_admin_disabled_without_configuration(tmp_path):
    app = create_app({"TESTING": True, "SECRET_KEY": "k", "DATABASE_PATH": str(tmp_path / "x.db")})
    c = app.test_client()
    t = re.search(r'value="([0-9a-f]+)"', c.get("/login").get_data(as_text=True)).group(1)
    r = c.post("/login", data={"username": "", "password": "", "csrf_token": t})
    assert r.status_code == 200 and "Invalid" in r.get_data(as_text=True)


def test_missing_secret_key_fails_fast(tmp_path, monkeypatch):
    monkeypatch.delenv("FLASK_DEBUG", raising=False)
    from app.config import Config
    monkeypatch.setattr(Config, "SECRET_KEY", None)
    with pytest.raises(RuntimeError):
        create_app({"DATABASE_PATH": str(tmp_path / "x.db")})


def test_404_page(client):
    r = client.get("/nope")
    assert r.status_code == 404 and "does not exist" in r.get_data(as_text=True)
