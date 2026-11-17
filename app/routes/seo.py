"""Search-engine files, the Search Console check and redirects from the old site's URLs."""

from flask import Blueprint, Response, current_app, redirect, url_for

from .. import content

bp = Blueprint("seo", __name__)

# The earlier multi-page site used these URLs; keep them working.
LEGACY_REDIRECTS = {
    "/index.html": "public.index",
    "/pages/about": "public.about",
    "/pages/about.html": "public.about",
    "/pages/projects": "public.projects",
    "/pages/projects.html": "public.projects",
    "/pages/resume": "public.resume",
    "/pages/resume.html": "public.resume",
    "/pages/contact": "public.contact",
    "/pages/contact.html": "public.contact",
}


def _redirect_to(endpoint: str):
    def view():
        return redirect(url_for(endpoint), code=301)

    return view


for _path, _endpoint in LEGACY_REDIRECTS.items():
    bp.add_url_rule(
        _path, endpoint="legacy_" + _path.strip("/").replace("/", "_").replace(".", "_"),
        view_func=_redirect_to(_endpoint),
    )


@bp.get("/robots.txt")
def robots():
    site = current_app.config["SITE_URL"]
    body = f"User-agent: *\nAllow: /\nDisallow: /login\nDisallow: /dashboard\n\nSitemap: {site}/sitemap.xml\n"
    return Response(body, mimetype="text/plain")


@bp.get("/sitemap.xml")
def sitemap():
    site = current_app.config["SITE_URL"]
    pages = [
        ("public.index", {}, "1.0"),
        ("public.about", {}, "0.7"),
        ("public.projects", {}, "0.9"),
        *[("public.project_detail", {"slug": project["slug"]}, "0.6") for project in content.PROJECTS],
        ("public.skills", {}, "0.7"),
        ("public.resume", {}, "0.8"),
        ("public.contact", {}, "0.6"),
    ]
    urls = "".join(
        f"  <url><loc>{site}{url_for(endpoint, **values)}</loc><priority>{priority}</priority></url>\n"
        for endpoint, values, priority in pages
    )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n"
    )
    return Response(xml, mimetype="application/xml")


@bp.get("/google9e1b677973c92115.html")
def google_site_verification():
    """Keeps the existing Google Search Console verification working."""
    return Response("google-site-verification: google9e1b677973c92115.html", mimetype="text/html")


@bp.get("/favicon.ico")
def favicon():
    return redirect(url_for("static", filename="favicon.svg"), code=301)
