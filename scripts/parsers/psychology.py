import re

from .common import clean, is_bad_name, make_row, normalize_email, normalize_phone


TITLE_WORDS = [
    "Professor",
    "Associate Professor",
    "Assistant Professor",
    "Lecturer",
    "Department Chair",
    "Coordinator",
    "Manager",
    "Advisor",
]


def extract_title(text: str) -> str:
    for title in TITLE_WORDS:
        if title.lower() in text.lower():
            return title
    return ""


def parse_psychology(department, category, url, soup):
    rows = []

    blocks = soup.select("article, .node, .views-row, .person, .profile, .card, li, tr")

    for block in blocks:
        text = clean(block.get_text(" "))
        email = normalize_email(text)

        if not email:
            continue

        heading = block.find(["h1", "h2", "h3", "h4", "strong", "a"])
        name = clean(heading.get_text(" ")) if heading else ""

        if is_bad_name(name):
            # Try last-name-first pattern from text.
            name_match = re.search(r"\b([A-Z][a-zA-Z'’.-]+,\s+[A-Z][a-zA-Z'’.-]+(?:\s+[A-Z][a-zA-Z'’.-]+)?)\b", text)
            name = name_match.group(1) if name_match else ""

        if is_bad_name(name):
            continue

        title = extract_title(text)
        phone = normalize_phone(text)

        office = ""
        office_match = re.search(r"\b(?:EP|HSS|SCI|TH|BH|BUS|FA|HH|SEC)\s*\d+[A-Z]?\b", text)
        if office_match:
            office = office_match.group(0)

        rows.append(
            make_row(
                department,
                category,
                name,
                title,
                email,
                phone,
                office,
                url,
                "Psychology parser v0.5",
            )
        )

    return rows