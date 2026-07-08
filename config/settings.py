"""
CoSE Pulse Configuration
"""

# -----------------------------
# Project Information
# -----------------------------

PROJECT_NAME = "CoSE Pulse"
VERSION = "2.0.0"

# -----------------------------
# Seed Domains
# -----------------------------

SEED_DOMAINS = [
    # Primary
    "https://cose.sfsu.edu",
    # CoSE Departments
    "https://engineering.sfsu.edu",
    "https://cs.sfsu.edu",
    "https://math.sfsu.edu",
    "https://biology.sfsu.edu",
    "https://chemistry.sfsu.edu",
    "https://physics.sfsu.edu",
    "https://psychology.sfsu.edu",
    # Strategic Sources
    "https://asi.sfsu.edu",
    # University
    "https://www.sfsu.edu",
    "https://news.sfsu.edu",
]

# -----------------------------
# Allowed Domains
# -----------------------------

ALLOWED_DOMAINS = [
    "cose.sfsu.edu",
    "engineering.sfsu.edu",
    "cs.sfsu.edu",
    "math.sfsu.edu",
    "biology.sfsu.edu",
    "chemistry.sfsu.edu",
    "physics.sfsu.edu",
    "psychology.sfsu.edu",
    "asi.sfsu.edu",
    "www.sfsu.edu",
    "news.sfsu.edu",
]

# -----------------------------
# Ignore File Types
# -----------------------------

IGNORE_EXTENSIONS = [
    ".pdf",
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".svg",
    ".zip",
    ".doc",
    ".docx",
    ".ppt",
    ".pptx",
    ".xls",
    ".xlsx",
    ".mp4",
    ".mov",
]

# -----------------------------
# Crawl Limits
# -----------------------------

MAX_DEPTH = 5

MAX_PAGES = 150

REQUEST_DELAY = 1.0

TIMEOUT = 20

USER_AGENT = "CoSE Pulse Bot (+https://github.com/OscarTumushabeMadong/CoSE_Pulse)"
