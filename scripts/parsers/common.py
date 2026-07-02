import datetime
import re

TODAY = datetime.date.today().isoformat()

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@(?:mail\.)?sfsu\.edu", re.I)
PHONE_RE = re.compile(r"(?:\+1\s*)?\(?415\)?[-.\s]?\d{3}[-.\s]?\d{4}")

BAD_NAME_TERMS = {
    "leadership & staff",
    "current list of office hours",
    "consulting times",
    "faculty people listing",
    "department office",
    "view profile",
    "read more",
    "contact",
}


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\xa0", " ")).strip()


def normalize_email(text: str) -> str:
    match = EMAIL_RE.search(text or "")
    return match.group(0).lower() if match else ""


def normalize_phone(text: str) -> str:
    match = PHONE_RE.search(text or "")
    return match.group(0) if match else ""


def is_bad_name(name: str) -> bool:
    value = clean(name).lower()
    return not value or value in BAD_NAME_TERMS or "office hours" in value


def infer_contact_type(title: str, category: str) -> str:
    text = f"{title} {category}".lower()

    if "dean" in text:
        return "Dean"
    if "chair" in text:
        return "Department Chair"
    if "advisor" in text or "advising" in text:
        return "Advisor"
    if any(x in text for x in ["coordinator", "assistant", "analyst", "specialist", "staff", "manager"]):
        return "Staff"
    if any(x in text for x in ["professor", "lecturer", "faculty"]):
        return "Faculty"

    return "Unknown"


def quality(name: str, email: str, title: str) -> str:
    if name and email and title:
        return "Clean"
    if name and email:
        return "Partial"
    return "Needs Review"


def make_row(department, category, name, title, email, phone, office, url, notes=""):
    name = clean(name)
    title = clean(title)
    email = normalize_email(email)
    phone = normalize_phone(phone)
    office = clean(office)

    return {
        "Department": department,
        "Category": category,
        "Contact Type": infer_contact_type(title, category),
        "Quality": quality(name, email, title),
        "Name": name,
        "Title": title,
        "Email": email,
        "Phone": phone,
        "Office": office,
        "Source URL": url,
        "Date Collected": TODAY,
        "Notes": notes,
    }