"""Main navigation: one list, so every page shows the same menu."""

# (label, endpoint, endpoints that should highlight this item)
NAV_ITEMS = [
    ("Home", "public.index", ("public.index",)),
    ("About", "public.about", ("public.about",)),
    ("Projects", "public.projects", ("public.projects", "public.project_detail")),
    ("Skills", "public.skills", ("public.skills",)),
    ("Resume", "public.resume", ("public.resume",)),
    ("Contact", "public.contact", ("public.contact",)),
]


def build_nav(current_endpoint: str | None) -> list[dict]:
    return [
        {"label": label, "endpoint": endpoint, "active": current_endpoint in active_for}
        for label, endpoint, active_for in NAV_ITEMS
    ]
