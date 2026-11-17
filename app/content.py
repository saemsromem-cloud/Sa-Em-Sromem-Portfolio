"""Portfolio content: the single source of truth.

The web page (templates/index.html) and the resume PDF
(scripts/build_resume.py) both read from this file, so facts only need
to be corrected in one place.

Rule for editing: only add things that are true. Anything marked
TODO is waiting on information that is not in the project yet.
"""

PROFILE = {
    "name": "Sa Em Sromem",
    "title": "Aspiring Backend Developer",
    "location": "Phnom Penh, Cambodia",
    "email": "saemsromem@gmail.com",
    "phone": "071 9335 708",  # Shown on the PDF resume only, not on the website.
    "github": "https://github.com/saemsromem-cloud",
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

# level: "Working" = used in real projects; "Foundational" = used, still building confidence;
# "Learning" = actively studying, not yet used in a finished project.
SKILLS = [
    {
        "group": "Backend development",
        "items": [
            ("Python", "Working"),
            ("Flask", "Working"),
            ("MySQL", "Working"),
            ("SQL", "Working"),
            ("REST API design", "Learning"),
        ],
    },
    {
        "group": "Frontend fundamentals",
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
            ("VS Code", "Working"),
        ],
    },
    {
        "group": "Web tools",
        "items": [("Google Search Console", "Foundational")],
    },
]

PROJECTS = [
    {
        "name": "This Portfolio \u2013 Flask Backend",
        "kind": "Backend project",
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
        "repo": None,  # TODO: add the GitHub repository URL for this portfolio.
        "demo": None,
    },
    {
        "name": "IT Awareness Club",
        "kind": "Frontend project and Backend academic team project",
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
        "tech": ["HTML", "CSS", "JavaScript"],
        "image": "images/it-awareness-club.webp",
        "image_alt": "Screenshot of the IT Awareness Club website",
        "repo": "https://github.com/mut-soriya/it-awareness-club-project",
        "demo": "https://it-awareness-club-project.vercel.app/",
    },
    {
        "name": "Internship and Career Guide",
        "kind": "Academic team project",
        "summary": (
            "A website that gives students guidance on internships and careers."
        ),
        "features": [
            "Responsive layout with reusable components",
            "Planned tasks and shared code with teammates through Git and GitHub",
        ],
        "contribution": None,  # TODO: say what you personally built.
        "tech": ["HTML", "CSS", "Tailwind CSS", "JavaScript"],
        "image": None,
        "repo": "https://github.com/Group-WEP-Design-Project/Career_Guide_Website",
        "demo": "https://kamserksa.vercel.app/index.html",
    },
]

EDUCATION = {
    "school": "Passerelles numériques Cambodia (PNC)",
    "program": "Web Programming",
    "years": "2026 to 2027 (expected graduation)",
    "expected_graduation": "2027",
    "level": "First-year student",
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

LANGUAGES = [("Khmer", "Native"), ("English", "Working proficiency")]
