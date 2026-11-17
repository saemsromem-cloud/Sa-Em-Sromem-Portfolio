import re

import pytest
from werkzeug.security import generate_password_hash

from app import content, create_app


@pytest.fixture()
def app(tmp_path):
    return create_app({
        "TESTING": True,
        "SECRET_KEY": "test-secret",
        "DATABASE_PATH": str(tmp_path / "test.db"),
        "SITE_URL": "https://example.test",
        "CONTACT_MIN_SECONDS": 0,
        "ADMIN_USERNAME": "owner",
        "ADMIN_PASSWORD_HASH": generate_password_hash("correct horse battery"),
    })


@pytest.fixture()
def client(app):
    return app.test_client()


def token(client, path="/"):
    html = client.get(path).get_data(as_text=True)
    match = re.search(r'name="csrf_token" value="([0-9a-f]+)"', html)
    assert match is not None
    return match.group(1)


VALID = {"name": "Dara", "email": "dara@example.com", "subject": "Internship", "message": "We would like to talk."}


PAGES = ["/", "/about", "/projects", "/skills", "/resume", "/contact"]


@pytest.mark.parametrize("path", PAGES)
def test_every_page_loads_with_seo_and_nav(client, path):
    resp = client.get(path)
    assert resp.status_code == 200
    html = resp.get_data(as_text=True)
    assert "<title>" in html and 'name="description"' in html
    assert 'rel="canonical"' in html and 'property="og:image"' in html
    for label in ["Home", "About", "Projects", "Skills", "Resume", "Contact"]:
        assert f">{label}</a>" in html
    assert html.count('aria-current="page"') == 1


def test_active_nav_item_follows_page(client):
    html = client.get("/skills").get_data(as_text=True)
    assert '<a href="/skills" class="is-current" aria-current="page">Skills</a>' in html
    detail = client.get("/projects/shoes-store").get_data(as_text=True)
    assert 'href="/projects" class="is-current"' in detail


def test_home_has_required_content(client):
    html = client.get("/").get_data(as_text=True)
    for text in ["Aspiring Backend Developer", "Download resume", "View my projects", "Contact me",
                 "Core skills", "Selected projects", "About me", "Passerelles"]:
        assert text in html


def test_all_projects_listed_and_have_detail_pages(client):
    page = client.get("/projects").get_data(as_text=True)
    for project in content.PROJECTS:
        assert project["name"] in page
        assert client.get(f"/projects/{project['slug']}").status_code == 200
    names = [p["name"] for p in content.PROJECTS]
    for expected in ["Personal Portfolio Website", "IT Awareness Club", "Shoes Store Website",
                     "Discover Ratanakiri", "Internship and Career Guide"]:
        assert expected in names


def test_unknown_project_is_404(client):
    assert client.get("/projects/does-not-exist").status_code == 404


def test_project_images_exist():
    from pathlib import Path
    static = Path(__file__).resolve().parent.parent / "app" / "static"
    for project in content.PROJECTS:
        if project["image"]:
            assert (static / project["image"]).is_file(), project["image"]


def test_projects_without_links_show_no_empty_buttons(client):
    html = client.get("/projects/discover-ratanakiri").get_data(as_text=True)
    assert "GitHub repository" not in html and "Live demo" not in html


def test_skills_page_separates_learning(client):
    html = client.get("/skills").get_data(as_text=True)
    assert "Currently learning" in html and "REST API design" in html
    assert "%" not in html.split("<main")[1].split("</main>")[0]  # no percentage skill bars


def test_resume_page_has_both_actions_and_no_phone(client):
    html = client.get("/resume").get_data(as_text=True)
    assert "Download PDF" in html and "Print resume" in html and 'class="cv"' in html
    assert "9335" not in html


def test_phone_number_not_on_website(client):
    for path in PAGES:
        assert "9335" not in client.get(path).get_data(as_text=True)


def test_resume_pdf_inline_and_download(client):
    inline = client.get("/resume.pdf")
    assert inline.status_code == 200 and inline.mimetype == "application/pdf" and inline.data.startswith(b"%PDF")
    download = client.get("/resume/download")
    assert "attachment" in download.headers["Content-Disposition"]


def test_seo_files(client):
    assert "https://example.test/sitemap.xml" in client.get("/robots.txt").get_data(as_text=True)
    sitemap = client.get("/sitemap.xml").get_data(as_text=True)
    for path in ["/", "/about", "/projects", "/skills", "/resume", "/contact", "/projects/shoes-store"]:
        assert f"<loc>https://example.test{path}</loc>" in sitemap
    assert client.get("/google9e1b677973c92115.html").status_code == 200


def test_legacy_urls_redirect_to_new_pages(client):
    for old, new in [("/pages/projects.html", "/projects"), ("/pages/about", "/about"),
                     ("/pages/contact.html", "/contact"), ("/pages/resume", "/resume"), ("/index.html", "/")]:
        r = client.get(old)
        assert r.status_code == 301 and r.headers["Location"].endswith(new)


def test_security_headers(client):
    headers = client.get("/").headers
    assert headers["X-Content-Type-Options"] == "nosniff" and headers["X-Frame-Options"] == "SAMEORIGIN"


def test_contact_page_has_form(client):
    html = client.get("/contact").get_data(as_text=True)
    for text in ['name="name"', 'name="email"', 'name="subject"', 'name="message"', 'name="website"', "github.com/"]:
        assert text in html


def test_contact_saves_message(client, app):
    r = client.post("/contact", data={**VALID, "csrf_token": token(client, "/contact")})
    assert r.status_code == 302 and r.headers["Location"].endswith("#form-status")
    assert "your message was sent" in client.get("/contact").get_data(as_text=True).lower()
    with app.app_context():
        from app.db import get_db
        rows = get_db().execute("SELECT * FROM messages").fetchall()
    assert len(rows) == 1 and rows[0]["status"] == "Unread"


def test_contact_rejects_invalid_input(client):
    r = client.post("/contact", data={**VALID, "email": "nope", "csrf_token": token(client, "/contact")})
    assert r.status_code == 400 and "valid email" in r.get_data(as_text=True)
    assert 'value="Dara"' in r.get_data(as_text=True)  # the form keeps what was typed


def test_contact_requires_csrf_token(client):
    assert client.post("/contact", data=VALID).status_code == 400


def test_contact_honeypot_discards_bots(client, app):
    client.post("/contact", data={**VALID, "website": "http://spam", "csrf_token": token(client, "/contact")})
    with app.app_context():
        from app.db import get_db
        assert get_db().execute("SELECT COUNT(*) FROM messages").fetchone()[0] == 0


def test_contact_rejects_too_many_links(client):
    spam = "http://a.example http://b.example http://c.example"
    r = client.post("/contact", data={**VALID, "message": spam, "csrf_token": token(client, "/contact")})
    assert r.status_code == 400 and "links" in r.get_data(as_text=True)


def test_contact_rejects_instant_submissions(tmp_path):
    app = create_app({"TESTING": True, "SECRET_KEY": "k", "DATABASE_PATH": str(tmp_path / "s.db"), "CONTACT_MIN_SECONDS": 60})
    c = app.test_client()
    r = c.post("/contact", data={**VALID, "csrf_token": token(c, "/contact")})
    assert r.status_code == 400 and "too quickly" in r.get_data(as_text=True)


def test_contact_double_submit_is_stored_once(client, app):
    for _ in range(2):
        client.post("/contact", data={**VALID, "csrf_token": token(client, "/contact")})
    with app.app_context():
        from app.db import get_db
        assert get_db().execute("SELECT COUNT(*) FROM messages").fetchone()[0] == 1


def test_contact_flood_limit(tmp_path):
    app = create_app({"TESTING": True, "SECRET_KEY": "k", "DATABASE_PATH": str(tmp_path / "f.db"),
                      "CONTACT_MIN_SECONDS": 0, "CONTACT_RECENT_LIMIT": 2})
    c = app.test_client()
    codes = []
    for i in range(3):
        r = c.post("/contact", data={**VALID, "subject": f"Hello {i}", "csrf_token": token(c, "/contact")})
        codes.append(r.status_code)
    assert codes == [302, 302, 429]


def test_sql_injection_text_is_stored_as_plain_text(client, app):
    payload = "x'); DROP TABLE messages;--"
    client.post("/contact", data={**VALID, "subject": payload, "csrf_token": token(client, "/contact")})
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
    client.post("/contact", data={**VALID, "csrf_token": token(client, "/contact")})
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
    match = re.search(r'value="([0-9a-f]+)"', c.get("/login").get_data(as_text=True))
    assert match is not None
    t = match.group(1)
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
