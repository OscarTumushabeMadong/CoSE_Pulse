import re

from .common import clean, make_row, normalize_email, normalize_phone


def parse_engineering(department, category, url, soup):
    rows = []

    blocks = soup.select("article, .node, .views-row, .person, .profile, .card, li, tr")

    for block in blocks:
        text = clean(block.get_text(" "))
        email = normalize_email(text)

        if not email:
            continue

        heading = block.find(["h1", "h2", "h3", "h4", "strong", "a"])
        name = clean(heading.get_text(" ")) if heading else ""

        if "@" in name or len(name.split()) > 8:
            name = ""

        phone = normalize_phone(text)

        office = ""
        office_match = re.search(
            r"Office:\s*([^|]+?)(?:Phone:|Email:|Fax:|$)", text, re.I
        )
        if office_match:
            office = office_match.group(1)

        title = text
        if name:
            title = title.replace(name, "", 1)

        title = re.sub(r"Office:.*", "", title, flags=re.I)
        title = re.sub(r"Phone:.*", "", title, flags=re.I)
        title = re.sub(r"Fax:.*", "", title, flags=re.I)
        title = re.sub(r"Email:.*", "", title, flags=re.I)
        title = clean(title)

        rows.append(
            make_row(department, category, name, title, email, phone, office, url)
        )

    return rows
