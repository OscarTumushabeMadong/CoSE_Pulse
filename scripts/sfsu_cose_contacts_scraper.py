import csv
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from parsers.common import clean, make_row
from parsers.engineering import parse_engineering
from parsers.normalizer import normalize_rows
from parsers.psychology import parse_psychology
from parsers.validator import validate


PROJECT_ROOT = Path(__file__).resolve().parents[1]

OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

RAW_OUTPUT_FILE = OUTPUT_DIR / "sfsu_cose_contacts_raw.csv"
REVIEW_OUTPUT_FILE = OUTPUT_DIR / "sfsu_cose_contacts_review.csv"
CLEAN_OUTPUT_FILE = OUTPUT_DIR / "sfsu_cose_contacts_clean.csv"

SEED_PAGES = [
    ("College of Science & Engineering", "Dean's Office", "https://cose.sfsu.edu/contact-us"),
    ("School of Engineering", "Staff", "https://engineering.sfsu.edu/staff"),
    ("School of Engineering", "Faculty", "https://engineering.sfsu.edu/faculty"),
    ("Computer Science", "People", "https://cs.sfsu.edu/people"),
    ("Biology", "People", "https://biology.sfsu.edu/people"),
    ("Physics & Astronomy", "Faculty", "https://physics.sfsu.edu/faculty"),
    ("Mathematics", "People", "https://math.sfsu.edu/faculty_gtas"),
    ("Mathematics", "Staff", "https://math.sfsu.edu/staff"),
    ("Chemistry & Biochemistry", "Faculty", "https://chemistry.sfsu.edu/faculty/"),
    ("Psychology", "Faculty & Staff", "https://psychology.sfsu.edu/faculty-staff"),
    ("Psychology", "Faculty Advisors", "https://psychology.sfsu.edu/faculty-faculty-advisors"),
]


def get_soup(url):
    headers = {
        "User-Agent": "Mozilla/5.0 academic-contact-research/1.0"
    }
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def parse_cose_deans(department, category, url, soup):
    text = clean(soup.get_text(" "))

    known_rows = [
        ("Carmen Domingo", "Dean of College of Science & Engineering", "cdomingo@sfsu.edu", ""),
        ("Ron Marzke", "Associate Dean of College of Science & Engineering", "marzke@sfsu.edu", ""),
        ("Teaster Baird", "Associate Dean of College of Science & Engineering", "tbaird@sfsu.edu", ""),
        ("Caroline Alcantara", "Assistant to the Dean", "caroline@sfsu.edu", "(415) 338-7660"),
        ("Elizabeth Detrich", "Personnel Analyst", "edetrich@sfsu.edu", ""),
        ("Queenie Cheng", "Academic Admin Analyst", "qcheng@sfsu.edu", "(415) 405-3771"),
        ("Lynne Hoang", "Employment Analyst", "lynnethi@sfsu.edu", "(415) 338-7696"),
        ("Crystal Kam", "College Business Officer", "crystalk@sfsu.edu", "(415) 338-2427"),
        ("Nicholas Christopher Kincaid", "Lead Accounting Specialist", "nicholas@sfsu.edu", ""),
        ("Jennifer Mueller", "Personnel Officer", "muellerj@sfsu.edu", "(415) 338-7659"),
        ("Lannie Nguyen", "Administrative & Events Assistant", "lannie@sfsu.edu", "(415) 338-7662"),
        ("Adria O'Dea", "Graphics Coordinator", "adria@sfsu.edu", ""),
        ("Nam Pham", "Fiscal Operations Specialist", "npham9@sfsu.edu", ""),
        ("Dominic Sciucchetti", "Operations Coordinator", "dominics@sfsu.edu", ""),
        ("Tracy Thai", "Administrative Specialist", "tthai@sfsu.edu", "(415) 338-7695"),
        ("Jenny Tu", "Senior Financial Operations Analyst", "jennytu@sfsu.edu", ""),
        ("Minling Zhang", "Senior Budget & Fiscal Analyst", "mzhang8@sfsu.edu", ""),
        ("Holly Fincke", "Senior Director of Development", "hollyfincke@sfsu.edu", ""),
    ]

    return [
        make_row(department, category, name, title, email, phone, "", url)
        for name, title, email, phone in known_rows
        if email in text
    ]


def parse_generic(department, category, url, soup):
    from parsers.common import normalize_email, normalize_phone

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

        title = text.replace(name, "", 1) if name else text
        title = title.replace(email, "")
        title = clean(title)

        rows.append(
            make_row(
                department=department,
                category=category,
                name=name,
                title=title,
                email=email,
                phone=normalize_phone(text),
                office="",
                url=url,
                notes="Generic parser v1.0",
            )
        )

    return rows


def route_parser(department, category, url, soup):
    if "cose.sfsu.edu/contact-us" in url:
        return parse_cose_deans(department, category, url, soup)

    if "engineering.sfsu.edu" in url:
        return parse_engineering(department, category, url, soup)

    if "psychology.sfsu.edu" in url:
        return parse_psychology(department, category, url, soup)

    return parse_generic(department, category, url, soup)


def deduplicate(rows):
    seen = {}

    for row in rows:
        email = row.get("Email", "").lower()

        if not email:
            continue

        score = sum(bool(row.get(k)) for k in ["Name", "Title", "Phone", "Office"])
        score += {"Clean": 3, "Partial": 2, "Needs Review": 1}.get(row.get("Quality", ""), 0)

        if email not in seen or score > seen[email][0]:
            seen[email] = (score, row)

    return sorted(
        [item[1] for item in seen.values()],
        key=lambda row: (
            row.get("Department", ""),
            row.get("Contact Type", ""),
            row.get("Name", ""),
        ),
    )


def write_csv(file_path, rows, fieldnames):
    with file_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    all_rows = []

    for department, category, url in SEED_PAGES:
        try:
            print(f"Scraping: {url}")
            soup = get_soup(url)
            all_rows.extend(route_parser(department, category, url, soup))
        except Exception as error:
            print(f"ERROR scraping {url}: {error}")

    fieldnames = [
        "Department",
        "Category",
        "Contact Type",
        "Quality",
        "Confidence",
        "Name",
        "First Name",
        "Last Name",
        "Title",
        "Email",
        "Generic Email",
        "Phone",
        "Office",
        "Source URL",
        "Date Collected",
        "Notes",
    ]

    raw_rows = normalize_rows(deduplicate(all_rows))
    validated_rows = validate(raw_rows)

    clean_rows = [
        row for row in validated_rows
        if int(row.get("Confidence", 0)) >= 80
    ]

    review_rows = [
        row for row in validated_rows
        if 50 <= int(row.get("Confidence", 0)) < 80
    ]

    write_csv(RAW_OUTPUT_FILE, raw_rows, fieldnames)
    write_csv(REVIEW_OUTPUT_FILE, review_rows, fieldnames)
    write_csv(CLEAN_OUTPUT_FILE, clean_rows, fieldnames)

    print(f"Raw contacts: {len(raw_rows)} -> {RAW_OUTPUT_FILE}")
    print(f"Review contacts: {len(review_rows)} -> {REVIEW_OUTPUT_FILE}")
    print(f"Clean contacts: {len(clean_rows)} -> {CLEAN_OUTPUT_FILE}")


if __name__ == "__main__":
    main()