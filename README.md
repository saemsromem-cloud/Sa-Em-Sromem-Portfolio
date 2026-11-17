# Sa Em Sromem: Backend Developer Portfolio

Personal portfolio built with **Python, Flask and SQLite**. It has six pages (Home, About, Projects with a detail page per project, Skills, Resume, Contact), a working contact form, a print-ready resume page with a PDF download, and a private admin dashboard for reading messages.

## Pages and URLs

| URL | Page |
|---|---|
| `/` | Home |
| `/about` | About me |
| `/projects`, `/projects/<slug>` | Project gallery and detail pages |
| `/skills` | Skills, labelled by how I use them |
| `/resume` | Resume (A4 page, Print button) |
| `/resume.pdf`, `/resume/download` | The PDF, opened or downloaded |
| `/contact` | Contact details and form |
| `/login`, `/dashboard` | Private admin area |

URLs from the earlier multi-page site (`/pages/about.html`, ...) redirect to the matching new page.

## Project structure

```
app/
  __init__.py        App factory: config, database, navigation, security headers, error pages
  config.py          Settings read from environment variables
  content.py         All portfolio text (profile, skills, projects). Edit this to update the site, the resume page AND the PDF.
  forms.py           Contact form validation and spam checks
  navigation.py      The menu, defined once
  db.py              SQLite connection, schema, message queries
  security.py        CSRF protection
  routes/public.py   Pages, resume files, contact form
  routes/seo.py      robots.txt, sitemap.xml, Search Console file, redirects from old URLs
  routes/admin.py    Login, dashboard, mark read, delete
  templates/         base.html (menu + footer), one template per page, _components.html (shared pieces)
  static/            css/site.css, css/resume.css, js, fonts (self-hosted), images, resume PDF
scripts/
  build_resume.py             Regenerates the resume PDF from app/content.py
  generate_password_hash.py   Creates the admin password hash
tests/test_app.py    Automated tests
wsgi.py              Production entry point (gunicorn)
```

## Run locally

Requires Python 3.10 or newer.

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt

cp .env.example .env               # Windows: copy .env.example .env
```

Edit `.env`:

1. `SECRET_KEY`: run `python -c "import secrets; print(secrets.token_hex(32))"` and paste the result.
2. `ADMIN_USERNAME`: choose a username.
3. `ADMIN_PASSWORD_HASH`: run `python scripts/generate_password_hash.py` and paste the line it prints.
4. For local work also add `FLASK_DEBUG=1`.

Start the site:

```bash
flask --app wsgi run --debug
```

Open http://127.0.0.1:5000. The admin dashboard is at http://127.0.0.1:5000/login.

## Update content and resume

- Edit `app/content.py`. Anything set to `None` (for example a project's `repo`, `demo` or `image`) is simply hidden on the site until you fill it in.
- Project screenshots go in `app/static/images/` (about 1200 px wide, `.webp`), then set the project's `image` path.
- Rebuild the resume PDF: `python scripts/build_resume.py`
- Run the tests: `python -m pytest`

## Deploy

**Netlify and Vercel host static files only, so they cannot run this Flask app or save contact messages.** Use a host that runs Python. The steps below use AWS EC2 (Ubuntu), which matches the tools on the resume.

```bash
# On the server
sudo apt update && sudo apt install -y python3-venv nginx
git clone <your-repo-url> portfolio && cd portfolio
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
cp .env.example .env && nano .env     # set SECRET_KEY, admin values, SITE_URL=https://your-domain, SESSION_COOKIE_SECURE=true
```

Run it with gunicorn under systemd, in `/etc/systemd/system/portfolio.service`:

```ini
[Unit]
Description=Portfolio
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/portfolio
EnvironmentFile=/home/ubuntu/portfolio/.env
ExecStart=/home/ubuntu/portfolio/.venv/bin/gunicorn --workers 2 --bind 127.0.0.1:8000 wsgi:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable --now portfolio
```

Point nginx at it (`/etc/nginx/sites-available/portfolio`, then link it into `sites-enabled` and reload):

```nginx
server {
    server_name your-domain;
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Add HTTPS with `sudo apt install certbot python3-certbot-nginx && sudo certbot --nginx`. Then open ports 80 and 443 in the EC2 security group.

After deploying: set `SITE_URL` to the real address, and in Google Search Console submit `/sitemap.xml`. The existing Search Console verification file is still served.

Back up `instance/messages.db`; it holds the contact messages.

## Security notes

- Secrets live in `.env` (ignored by git), never in the code. The app refuses to start without `SECRET_KEY`.
- Admin login is disabled until `ADMIN_USERNAME` and `ADMIN_PASSWORD_HASH` are set.
- All forms use CSRF tokens; database queries are parameterized.
- Contact form spam protection: hidden honeypot field, a minimum fill-in time (`CONTACT_MIN_SECONDS`, default 3), a limit of 2 links per message, double-submit detection, and a cap on messages per time window (`CONTACT_RECENT_LIMIT` per `CONTACT_RECENT_MINUTES`, default 10 per 10 minutes).
- Not included yet: login rate limiting. Put `fail2ban` or nginx `limit_req` in front of `/login` if the site gets real traffic.
