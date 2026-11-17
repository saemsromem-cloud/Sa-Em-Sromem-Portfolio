"""Build the portfolio resume PDF from app/content.py.

Usage:  python scripts/build_resume.py
Output: app/static/resume/Sa-Em-Sromem-Resume.pdf
"""

import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    FrameBreak,
    HRFlowable,
    KeepTogether,
    NextPageTemplate,
    PageTemplate,
    Paragraph,
    Spacer,
)

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from app import content  # noqa: E402

OUTPUT = ROOT / "app" / "static" / "resume" / "Sa-Em-Sromem-Resume.pdf"
FONT_DIR = Path(__file__).resolve().parent / "fonts"
PROFILE_IMAGE = ROOT / "app" / "static" / "images" / "profile.jpg"

NAVY = colors.HexColor("#1c344b")
INK = colors.HexColor("#172638")
MUTED = colors.HexColor("#526274")
SIDEBAR_TEXT = colors.HexColor("#eaf0f4")
SIDEBAR_MUTED = colors.HexColor("#bdcbd5")
ACCENT = colors.HexColor("#71d1bd")
RULE = colors.HexColor("#cdd5dc")
PAGE_WIDTH, PAGE_HEIGHT = A4
SIDEBAR_X = 4 * mm
SIDEBAR_WIDTH = 76 * mm
MAIN_X = 88 * mm
MAIN_WIDTH = PAGE_WIDTH - MAIN_X - 8 * mm

pdfmetrics.registerFont(TTFont("Body", str(FONT_DIR / "LiberationSans-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Body-Bold", str(FONT_DIR / "LiberationSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Body-Italic", str(FONT_DIR / "LiberationSans-Italic.ttf")))
pdfmetrics.registerFontFamily(
    "Body",
    normal="Body",
    bold="Body-Bold",
    italic="Body-Italic",
    boldItalic="Body-Bold",
)


def style(name: str, **overrides) -> ParagraphStyle:
    base = {
        "fontName": "Body",
        "fontSize": 8.7,
        "leading": 11.4,
        "textColor": INK,
        "alignment": TA_LEFT,
    }
    return ParagraphStyle(name, **{**base, **overrides})


S = {
    "name": style("name", fontSize=29, leading=33, textColor=INK),
    "title": style(
        "title",
        fontName="Body-Bold",
        fontSize=10.2,
        leading=13.8,
        textColor=colors.HexColor("#356a78"),
        spaceAfter=2,
    ),
    "heading": style(
        "heading",
        fontName="Body-Bold",
        fontSize=10.3,
        leading=13,
        textColor=INK,
        spaceBefore=9,
        spaceAfter=4,
    ),
    "body": style("body", fontSize=9.15, leading=12.8),
    "project": style(
        "project",
        fontName="Body-Bold",
        fontSize=10,
        leading=12.8,
        spaceBefore=6,
        spaceAfter=1.5,
    ),
    "meta": style("meta", fontSize=8.2, leading=10.6, textColor=MUTED, spaceAfter=1.4),
    "bullet": style(
        "bullet",
        fontSize=8.8,
        leading=12,
        leftIndent=10,
        bulletIndent=0,
        spaceAfter=1,
    ),
    "side_heading": style(
        "side_heading",
        fontName="Body-Bold",
        fontSize=9,
        leading=12,
        textColor=colors.white,
        spaceBefore=9,
        spaceAfter=3,
    ),
    "side_body": style(
        "side_body",
        fontSize=8.3,
        leading=11.4,
        textColor=SIDEBAR_TEXT,
        spaceAfter=2.5,
        splitLongWords=1,
    ),
    "side_bullet": style(
        "side_bullet",
        fontSize=8.2,
        leading=11.3,
        textColor=SIDEBAR_TEXT,
        leftIndent=8,
        bulletIndent=0,
        spaceAfter=1.4,
    ),
    "side_label": style(
        "side_label",
        fontName="Body-Bold",
        fontSize=7.2,
        leading=9,
        textColor=ACCENT,
        spaceBefore=4,
        spaceAfter=1,
    ),
}


def esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def section_heading(text: str, sidebar: bool = False) -> list:
    heading_style = S["side_heading"] if sidebar else S["heading"]
    line_color = colors.HexColor("#77909f") if sidebar else RULE
    return [
        Paragraph(esc(text).upper(), heading_style),
        HRFlowable(
            width="100%",
            thickness=0.55,
            color=line_color,
            spaceBefore=0,
            spaceAfter=3,
        ),
    ]


def project_bullets(project: dict) -> list[str]:
    if project.get("resume_bullets"):
        return project["resume_bullets"]
    bullets = [project["contribution"]] if project["contribution"] else []
    return bullets + project["features"][: 3 - len(bullets)]


def project_block(project: dict) -> list:
    block = [
        Paragraph(esc(project["name"]), S["project"]),
        Paragraph(
            f'<font name="Body-Bold">{esc(project["kind"])}</font>'
            f' | {esc(", ".join(project["tech"]))}',
            S["meta"],
        ),
    ]
    block.extend(
        Paragraph(esc(bullet), S["bullet"], bulletText="\u2022")
        for bullet in project_bullets(project)
    )
    links = []
    for label, field in (("Repository", "repo"), ("Live demo", "demo")):
        url = project.get(field)
        if url:
            visible_url = url.replace("https://", "").replace("http://", "").rstrip("/")
            links.append(
                f'<link href="{esc(url)}" color="{ACCENT.hexval()}">'
                f'{label}: {esc(visible_url)}</link>'
            )
    if links:
        block.append(Paragraph(" | ".join(links), S["meta"]))
    return block


def draw_page(canvas, _doc) -> None:
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(SIDEBAR_X, 5 * mm, SIDEBAR_WIDTH, PAGE_HEIGHT - 10 * mm, fill=1, stroke=0)

    diameter = 34 * mm
    image_x = SIDEBAR_X + (SIDEBAR_WIDTH - diameter) / 2
    image_y = PAGE_HEIGHT - 12 * mm - diameter
    image_path = canvas.beginPath()
    image_path.circle(image_x + diameter / 2, image_y + diameter / 2, diameter / 2)
    canvas.saveState()
    canvas.clipPath(image_path, stroke=0, fill=0)
    canvas.drawImage(
        ImageReader(str(PROFILE_IMAGE)),
        image_x,
        image_y,
        width=diameter,
        height=diameter,
        preserveAspectRatio=True,
        mask="auto",
    )
    canvas.restoreState()
    canvas.setStrokeColor(colors.white)
    canvas.setLineWidth(1.1)
    canvas.circle(image_x + diameter / 2, image_y + diameter / 2, diameter / 2, stroke=1, fill=0)
    canvas.restoreState()


def sidebar_story(profile: dict) -> list:
    github = profile["github"].replace("https://", "").rstrip("/")
    linkedin = profile["linkedin"].replace("https://www.", "").rstrip("/")
    link_color = ACCENT.hexval()
    items = section_heading("Contact", sidebar=True)
    items.extend(
        [
            Paragraph(esc(profile["phone"]), S["side_body"]),
            Paragraph(
                f'<link href="mailto:{esc(profile["email"])}" color="{link_color}">'
                f'{esc(profile["email"])}</link>',
                S["side_body"],
            ),
            Paragraph(esc(profile["location"]), S["side_body"]),
            Paragraph(
                f'<link href="{esc(profile["github"])}" color="{link_color}">'
                f'{esc(github)}</link>',
                S["side_body"],
            ),
            Paragraph(
                f'<link href="{esc(profile["linkedin"])}" color="{link_color}">'
                f'{esc(linkedin)}</link>',
                S["side_body"],
            ),
            Spacer(1, 3 * mm),
        ]
    )

    items.extend(section_heading("Technical skills", sidebar=True))
    for label, group_name in [
        ("Backend", "backend development"),
        ("Frontend", "frontend fundamentals"),
        ("Tools & Deployment", "tools and deployment"),
    ]:
        group = next(group for group in content.SKILLS if group["group"].lower() == group_name)
        values = [
            f"{name} (currently learning)" if level == "Learning" else name
            for name, level in group["items"]
        ]
        if label == "Tools & Deployment":
            web_tools = next(group for group in content.SKILLS if group["group"] == "Web tools")
            values.extend(name for name, _level in web_tools["items"])
        items.append(Paragraph(esc(label.upper()), S["side_label"]))
        items.extend(
            Paragraph(
                esc(value),
                S["side_bullet"],
                bulletText="\u2022",
            )
            for value in values
        )

    items.append(Spacer(1, 64 * mm))
    items.extend(section_heading("Languages", sidebar=True))
    items.extend(
        Paragraph(f"{esc(language)}: {esc(level)}", S["side_body"])
        for language, level in content.LANGUAGES
    )
    return items


def main_story(profile: dict) -> list:
    story = [
        Paragraph(
            'Sa Em <font name="Body-Bold">Sromem</font>',
            S["name"],
        ),
        Paragraph(esc(profile["title"].upper()), S["title"]),
        Spacer(1, 5 * mm),
        HRFlowable(width="100%", thickness=1.1, color=colors.HexColor("#356a78"), spaceAfter=2),
    ]
    story.extend(section_heading("Professional summary"))
    story.append(Paragraph(esc(content.SUMMARY), S["body"]))

    projects = [project_block(project) for project in content.PROJECTS]
    story.append(KeepTogether(section_heading("Projects") + projects[0] + [Spacer(1, 1.5 * mm)]))
    story.extend(KeepTogether(block + [Spacer(1, 1.5 * mm)]) for block in projects[1:])

    story.extend(section_heading("Education"))
    education = content.EDUCATION
    story.extend(
        [
            Paragraph(esc(education["school"]), S["project"]),
            Paragraph(
                f'{esc(education["program"])}'
                f' | {esc(education["level"])}'
                f' | Expected graduation: {esc(education["expected_graduation"])}',
                S["meta"],
            ),
        ]
    )
    return story


def build() -> Path:
    profile = content.PROFILE
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    doc = BaseDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        title=f"{profile['name']} - Resume",
        author=profile["name"],
        subject="Backend Developer internship application",
        creator="scripts/build_resume.py",
    )
    sidebar_frame = Frame(
        SIDEBAR_X,
        5 * mm,
        SIDEBAR_WIDTH,
        PAGE_HEIGHT - 10 * mm,
        leftPadding=7 * mm,
        rightPadding=7 * mm,
        topPadding=54 * mm,
        bottomPadding=8 * mm,
        id="sidebar",
    )
    main_frame = Frame(
        MAIN_X,
        8 * mm,
        MAIN_WIDTH,
        PAGE_HEIGHT - 16 * mm,
        leftPadding=0,
        rightPadding=0,
        topPadding=12 * mm,
        bottomPadding=8 * mm,
        id="main",
    )
    continuation_frame = Frame(
        16 * mm,
        12 * mm,
        PAGE_WIDTH - 32 * mm,
        PAGE_HEIGHT - 24 * mm,
        leftPadding=0,
        rightPadding=0,
        topPadding=4 * mm,
        bottomPadding=4 * mm,
        id="continuation",
    )
    doc.addPageTemplates(
        [
            PageTemplate(id="resume", frames=[sidebar_frame, main_frame], onPage=draw_page),
            PageTemplate(id="continuation", frames=[continuation_frame]),
        ]
    )

    story = [NextPageTemplate("continuation")]
    story.extend(sidebar_story(profile))
    story.append(FrameBreak())
    story.extend(main_story(profile))
    doc.build(story)
    return OUTPUT


if __name__ == "__main__":
    print(f"Wrote {build()}")
