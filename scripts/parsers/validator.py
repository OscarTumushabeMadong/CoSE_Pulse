import re

BAD_NAME_PATTERNS = [
    r"leadership\s*&\s*staff",
    r"faculty\s*&\s*staff$",
    r"current list",
    r"office hours",
    r"consulting",
    r"department office",
    r"faculty people",
    r"email:",
    r"phone:",
    r"view profile",
    r"read more",
]

TITLE_WORDS = [
    "Professor",
    "Dean",
    "Chair",
    "Coordinator",
    "Advisor",
    "Director",
    "Manager",
    "Lecturer",
    "Research",
    "Scientist",
    "Analyst",
    "Specialist",
    "Assistant",
]

EMAIL_RE = re.compile(r".+@.+")
PHONE_RE = re.compile(r"\d{3}[- )]\d{3}")

def confidence(row):

    score = 0

    if row["Name"]:
        score += 25

    if row["Title"]:
        score += 20

    if row["Email"]:
        score += 30

    if row["Phone"]:
        score += 10

    if row["Office"]:
        score += 10

    title = row["Title"]

    if any(word.lower() in title.lower() for word in TITLE_WORDS):
        score += 5

    return min(score,100)

def bad_name(name):

    name = name.lower()

    for pattern in BAD_NAME_PATTERNS:
        if re.search(pattern,name):
            return True

    return False

def validate(rows):

    cleaned = []

    for row in rows:

        if bad_name(row["Name"]):
            continue

        if EMAIL_RE.fullmatch(row["Name"]):
            continue

        if len(row["Name"].split()) > 8:
            continue

        if len(row["Title"].split()) > 25:
            continue

        row["Confidence"] = confidence(row)

        cleaned.append(row)

    return cleaned