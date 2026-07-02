import re


GENERIC_EMAIL_PREFIXES = {
    "cs-dept",
    "engrstaff",
    "biology",
    "chemistry",
    "physics",
    "math",
    "psychology",
}


TITLE_NORMALIZATIONS = {
    "prof.": "Professor",
    "professor.": "Professor",
    "associate professor": "Associate Professor",
    "assistant professor": "Assistant Professor",
    "lecturer": "Lecturer",
    "department chair": "Department Chair",
    "chair": "Department Chair",
    "coordinator": "Coordinator",
    "manager": "Manager",
    "advisor": "Advisor",
    "director": "Director",
    "analyst": "Analyst",
    "specialist": "Specialist",
}


def normalize_phone(phone: str) -> str:
    if not phone:
        return ""

    digits = re.sub(r"\D", "", phone)

    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]

    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"

    return phone.strip()


def normalize_title(title: str) -> str:
    if not title:
        return ""

    text = re.sub(r"\s+", " ", title).strip()
    lower = text.lower()

    for key, value in TITLE_NORMALIZATIONS.items():
        if key in lower:
            return value

    if len(text.split()) > 12:
        return ""

    return text


def split_name(name: str) -> tuple[str, str]:
    if not name:
        return "", ""

    name = name.strip()

    if "," in name:
        parts = [p.strip() for p in name.split(",", 1)]
        return parts[1], parts[0]

    parts = name.split()
    if len(parts) >= 2:
        return " ".join(parts[:-1]), parts[-1]

    return name, ""


def is_generic_email(email: str) -> bool:
    if not email or "@" not in email:
        return False

    prefix = email.split("@")[0].lower()
    return prefix in GENERIC_EMAIL_PREFIXES or "dept" in prefix or "office" in prefix


def normalize_rows(rows: list[dict]) -> list[dict]:
    normalized = []

    for row in rows:
        row = dict(row)

        row["Phone"] = normalize_phone(row.get("Phone", ""))
        row["Title"] = normalize_title(row.get("Title", ""))

        first_name, last_name = split_name(row.get("Name", ""))
        row["First Name"] = first_name
        row["Last Name"] = last_name

        row["Generic Email"] = "Yes" if is_generic_email(row.get("Email", "")) else "No"

        if row["Generic Email"] == "Yes":
            row["Notes"] = (row.get("Notes", "") + " Generic departmental email; do not treat as personal contact.").strip()

        normalized.append(row)

    return normalized