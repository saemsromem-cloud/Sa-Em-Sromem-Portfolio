"""Portfolio content: the single source of truth.

The website pages (templates/), the HTML resume page and the resume PDF
(scripts/build_resume.py) all read from this file, so a fact only needs to be
corrected in one place.

Rule for editing: only add things that are true. Anything set to None is
waiting on information that is not in the project yet, and the templates hide
it instead of showing an empty placeholder.
"""

PROFILE = {
    "name": "Sa Em Sromem",
    "initials": "SE",
    "title": "Aspiring Backend Developer",
    "location": "Phnom Penh, Cambodia",
    "email": "saemsromem@gmail.com",
    "phone": "068 795 467",  # Shown on the PDF resume only, not on the website.
    "github": "https://github.com/saemsromem-cloud",
    "github_handle": "saemsromem-cloud",
    "linkedin": "https://www.linkedin.com/in/sa-em-sromem-65ab73428/",
    "telegram": "https://t.me/Em_Programming",
    "telegram_handle": "@Em_Programming",
    "target": "Backend Developer internship, 2027",
    "intro": (
        "I build backend-focused web applications using Python and Flask, with "
        "an interest in database design, programming logic, and solving "
        "real-world problems. I am strengthening my backend skills and "
        "preparing for an internship in 2027."
    ),
}

SUMMARY = (
    "First-year Web Programming student at Passerelles numériques Cambodia (PNC) with a "
    "foundation in Python, JavaScript and SQL, and a strong interest in backend development "
    "and programming logic. Currently learning Flask and REST API development, and built "
    "a Flask project with a database and an admin dashboard. Seeking a Backend Developer "
    "internship in 2027 to contribute to a development team and keep learning."
)

# ---------------------------------------------------------------- About page

ABOUT = [
    "I study Web Programming at Passerelles numériques Cambodia (PNC) and "
    "expect to graduate in 2027. My goal is to become a backend developer.",
    "What draws me to backend work is the logic behind an application: how "
    "data is validated, stored and returned, and how a problem is broken into "
    "small steps that a program can follow. I enjoy algorithms and "
    "problem-solving for the same reason.",
    "I can build basic pages with HTML, CSS and JavaScript, but my focus is "
    "the server side: Python, Flask, SQL and, next, REST APIs.",
]

APPROACH = [
    (
        "Break the problem into steps",
        "Before I write code I describe what the program has to do in small "
        "steps, for example: check the input, store it, then return a result.",
    ),
    (
        "Learn by building",
        "I practise a topic by using it in a project. This portfolio started as "
        "static pages and grew into a Flask application with a database and an "
        "admin dashboard.",
    ),
    (
        "Work with other people",
        "On team projects I plan tasks with teammates and share code through "
        "Git and GitHub.",
    ),
]

GOAL = (
    "I am looking for a Backend Developer internship in 2027 where I can "
    "contribute to a development team, learn from experienced developers and "
    "keep improving my Python, Flask and database skills."
)

# ---------------------------------------------------------------- Skills page
# level: "Working" = used in real projects; "Foundational" = used, still building
# confidence; "Learning" = actively studying, not yet used in a finished project.

SKILL_LEVELS = {
    "Working": "Used in projects",
    "Foundational": "Foundational",
    "Learning": "Learning",
}

SKILL_LEVEL_HELP = {
    "Working": "I have used it in projects and can work with it day to day.",
    "Foundational": "I have used it and understand the basics, and I am still building confidence.",
    "Learning": "I am studying it now and have not used it in a finished project yet.",
}

SKILLS = [
    {
        "group": "Backend",
        "items": [
            ("Python", "Working"),
            ("Flask", "Working"),
            ("MySQL", "Working"),
            ("SQL", "Working"),
            ("REST API design", "Learning"),
        ],
    },
    {
        "group": "Frontend",
        "items": [
            ("HTML", "Working"),
            ("CSS", "Working"),
            ("JavaScript", "Foundational"),
            ("Tailwind CSS", "Foundational"),
        ],
    },
    {
        "group": "Tools and deployment",
        "items": [
            ("Git", "Working"),
            ("GitHub", "Working"),
            ("Linux / Ubuntu", "Foundational"),
            ("AWS EC2", "Foundational"),
            ("Vercel", "Working"),
            ("Netlify", "Working"),
            ("Google Search Console", "Foundational"),
        ],
    },
]

# Skills shown on the home page.
FEATURED_SKILLS = ["Python", "Flask", "SQL", "MySQL", "HTML", "CSS", "JavaScript", "Git", "GitHub"]

# A project's "tech" entry counts as use of these skills.
SKILL_ALIASES = {"SQL": ["SQL", "SQLite"]}

# ------------------------------------------------------------------ Projects
# "image" is a screenshot in static/images. Projects without one get a
# designed text cover instead of a broken or invented picture.

PROJECTS = [
    {
        "slug": "portfolio-website",
        "name": "Personal Portfolio Website",
        "kind": "Backend project",
        "featured": True,
        "summary": (
            "The site you are viewing is a Flask application. Visitors can send "
            "a message through the contact form, and I read and manage those "
            "messages in a private admin dashboard."
        ),
        "features": [
            "Server-side validation of every contact form field",
            "Messages stored in a SQLite database with parameterized queries",
            "Admin login with a hashed password, read from environment variables",
            "Dashboard to search, mark as read and delete messages",
            "CSRF protection on all forms; secrets kept out of the source code",
        ],
        "contribution": (
            "Designed and wrote the Flask routes, the database schema and the "
            "admin dashboard, and set up configuration through environment variables."
        ),
        "resume_bullets": [
            "Built a Flask application with routes, a SQLite database schema and a password-protected admin dashboard.",
            "Validated contact form input on the server and stored messages using parameterized SQL queries.",
            "Added CSRF protection and kept secrets and configuration in environment variables.",
        ],
        "tech": ["Python", "Flask", "SQLite", "Jinja2", "HTML", "CSS", "JavaScript"],
        "image": None,
        "image_alt": None,
        "repo": "https://github.com/saemsromem-cloud/Portfolio-Sa-Em-Sromem",
        "demo": None,
    },
    {
        "slug": "it-awareness-club",
        "name": "IT Awareness Club",
        "kind": "Academic team project",
        "featured": True,
        "summary": (
            "A website that shares IT news, activities, events and resources "
            "for students in one place."
        ),
        "features": [
            "Organized content sections",
            "Responsive page layout",
            "Reusable UI structure",
        ],
        "contribution": "Built the pages and layout with HTML, CSS and JavaScript.",
        "resume_bullets": [
            "Built the pages and layout of a website that shares IT news, activities, events and resources for students.",
            "Used HTML, CSS and JavaScript to create a responsive page layout.",
        ],
        "tech": ["HTML", "CSS", "JavaScript", "Vercel"],
        "image": "images/it-awareness-club.webp",
        "image_alt": "Screenshot of the IT Awareness Club website home page",
        "repo": "https://github.com/mut-soriya/it-awareness-club-project",
        "demo": "https://it-awareness-club-project.vercel.app/",
    },
    {
        "slug": "internship-career-guide",
        "name": "Internship and Career Guide",
        "kind": "Academic team project",
        "featured": True,
        "summary": (
            "A website that gives students guidance on internships and careers."
        ),
        "features": [
            "Responsive layout with reusable components",
            "Clean, accessible interface with consistent typography and color",
            "Tasks planned and code shared with teammates through Git and GitHub",
        ],
        "contribution": (
            "Worked with teammates to plan tasks and build website features, "
            "and used Git and GitHub for version control and collaboration."
        ),
        "resume_bullets": [
            "Worked in a team to build a website that gives students guidance on internships and careers.",
            "Applied responsive design and reusable components; used Git and GitHub to collaborate.",
        ],
        "tech": ["HTML", "CSS", "Tailwind CSS", "JavaScript", "Git", "GitHub", "Vercel"],
        "image": "images/career-guide.webp",
        "image_alt": "Screenshot of the Internship and Career Guide website home page",
        "repo": "https://github.com/Group-WEP-Design-Project/Career_Guide_Website",
        "demo": "https://kamserksa.vercel.app/index.html",
    },
]

# ----------------------------------------------------------------- Education

EDUCATION = {
    "school": "Passerelles numériques Cambodia (PNC)",
    "short_school": "PNC",
    "program": "Web Programming",
    "years": "2026 to present",
    "level": "second-year student",
    "topics": "Programming fundamentals, web development, databases, Linux and Git.",
}

LEARNING = {
    "now": [
        ("REST API design", "Learning how to design endpoints, status codes and JSON responses."),
        ("Flask application structure", "Organizing routes, configuration and templates so a project stays maintainable."),
        ("SQL and database design", "Writing queries and modeling tables for real data."),
        ("Linux and cloud basics", "Working with Ubuntu and AWS EC2."),
    ],
    "timeline": [
        ("Foundation", "Started with HTML, CSS and Python to learn structure, styling and programming basics."),
        ("Projects", "Built and deployed small websites, and worked with Git and GitHub on team projects."),
        ("Backend", "Built the Flask backend for this portfolio, including the database and admin dashboard."),
        ("Next", "Apply what I am learning about REST APIs in a Flask project."),
    ],
}

# Used by the resume page and the resume PDF.
LEARNING_EXPERIENCE = [
    "Built individual and team web projects as part of the Web Programming program at PNC.",
    "Used Git and GitHub to manage source code and work with teammates.",
    "Practised relational databases with MySQL, and worked with Linux / Ubuntu and basic cloud environments.",
    "Took part in team planning, discussions and presentations.",
]

TECHNICAL_BACKGROUND = (
    "Server side: Python and Flask applications with routes, form validation, CSRF protection "
    "and environment-based configuration, using SQLite and MySQL databases. "
    "Front end: responsive HTML, CSS and JavaScript, and Tailwind CSS. "
    "Tools: Git and GitHub, Linux / Ubuntu, AWS EC2, and hosting on Vercel and Netlify. "
    "Currently learning REST API design."
)

LANGUAGES = [("Khmer", "Native"), ("English", "Working proficiency")]


# ------------------------------------------------------------------- Helpers


def get_project(slug: str) -> dict | None:
    return next((project for project in PROJECTS if project["slug"] == slug), None)


def neighbour_projects(slug: str) -> tuple[dict | None, dict | None]:
    """Return the previous and next project, for the detail page links."""
    index = next((i for i, project in enumerate(PROJECTS) if project["slug"] == slug), None)
    if index is None:
        return None, None
    previous = PROJECTS[index - 1] if index > 0 else None
    following = PROJECTS[index + 1] if index < len(PROJECTS) - 1 else None
    return previous, following


def featured_projects() -> list[dict]:
    return [project for project in PROJECTS if project["featured"]]


def skill_level(name: str) -> str | None:
    for group in SKILLS:
        for skill, level in group["items"]:
            if skill == name:
                return level
    return None


def projects_using(skill: str) -> list[dict]:
    """Projects whose technology list shows this skill in use."""
    names = SKILL_ALIASES.get(skill, [skill])
    return [project for project in PROJECTS if any(tech in names for tech in project["tech"])]


def learning_skills() -> list[str]:
    return [name for group in SKILLS for name, level in group["items"] if level == "Learning"]
