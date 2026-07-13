"""
Priority scoring for discovered pages.
"""


def calculate_priority(row: dict) -> int:
    score = 0

    category = row.get("Category", "")
    opportunity = row.get("Opportunity Type", "")

    if category == "Scholarship":
        score += 100

    elif category == "Internship":
        score += 95

    elif category == "Research":
        score += 90

    elif category == "Career":
        score += 85

    elif category == "Event":
        score += 70

    elif category == "News":
        score += 50

    elif category == "Faculty & Staff":
        score += 20

    if opportunity == "Scholarship":
        score += 25

    elif opportunity == "Internship":
        score += 20

    elif opportunity == "Research":
        score += 15

    elif opportunity == "Career":
        score += 10

    if row.get("Deadline"):
        score += 20

    return min(score, 100)
