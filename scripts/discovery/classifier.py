"""
CoSE Pulse Discovery Classifier

Classifies discovered URLs into useful information categories.
"""

from urllib.parse import urlparse


CATEGORY_RULES = {
    "Event": [
        "event",
        "events",
        "calendar",
        "seminar",
        "workshop",
        "lecture",
        "symposium",
        "showcase",
    ],
    "Scholarship": [
        "scholarship",
        "scholarships",
        "financial-aid",
        "financialaid",
        "award",
        "awards",
    ],
    "Internship": [
        "internship",
        "internships",
        "career",
        "careers",
        "jobs",
        "employment",
        "opportunity",
        "opportunities",
    ],
    "Research": [
        "research",
        "lab",
        "labs",
        "centers-research",
        "center",
        "centers",
    ],
    "Faculty & Staff": [
        "faculty",
        "staff",
        "people",
        "directory",
    ],
    "Contact": [
        "contact",
        "contact-us",
    ],
    "News": [
        "news",
        "announcement",
        "announcements",
        "story",
        "stories",
    ],
    "Advising": [
        "advising",
        "advisor",
        "advisors",
        "student-resources",
        "resources",
    ],
    "Academics": [
        "academics",
        "programs",
        "courses",
        "degree",
        "degrees",
        "major",
        "minor",
        "graduate",
        "undergraduate",
    ],
    "Student Life": [
        "student",
        "students",
        "clubs",
        "organizations",
        "asi",
        "leadership",
    ],
}


DOMAIN_LABELS = {
    "cose.sfsu.edu": "College of Science & Engineering",
    "engineering.sfsu.edu": "School of Engineering",
    "cs.sfsu.edu": "Computer Science",
    "math.sfsu.edu": "Mathematics",
    "biology.sfsu.edu": "Biology",
    "chemistry.sfsu.edu": "Chemistry & Biochemistry",
    "physics.sfsu.edu": "Physics & Astronomy",
    "psychology.sfsu.edu": "Psychology",
    "asi.sfsu.edu": "Associated Students",
    "www.sfsu.edu": "San Francisco State University",
    "news.sfsu.edu": "SFSU News",
}


def get_department(url: str) -> str:
    domain = urlparse(url).netloc.lower()
    return DOMAIN_LABELS.get(domain, "Unknown")


def classify_url(url: str) -> tuple[str, int]:
    """
    Returns:
        category: best matching category
        confidence: rule-based confidence score from 0 to 100
    """

    parsed = urlparse(url)
    text = f"{parsed.netloc} {parsed.path}".lower()

    best_category = "General"
    best_score = 0

    for category, keywords in CATEGORY_RULES.items():
        score = 0

        for keyword in keywords:
            if keyword in text:
                score += 25

        if score > best_score:
            best_score = score
            best_category = category

    return best_category, min(best_score, 100)