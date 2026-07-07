"""
Opportunity extraction utilities for CoSE Pulse.

Extracts structured opportunity-like fields from discovered pages.
"""

import re
from bs4 import BeautifulSoup


DEADLINE_PATTERN = re.compile(
    r"(deadline|apply by|applications due|due date)[:\s\-]*"
    r"([A-Za-z]+\s+\d{1,2},?\s+\d{4})",
    re.IGNORECASE,
)

TIME_PATTERN = re.compile(
    r"\b\d{1,2}:\d{2}\s?(?:AM|PM|am|pm)\b"
)

MONEY_PATTERN = re.compile(
    r"\$\s?\d{1,3}(?:,\d{3})*(?:\.\d{2})?"
)


def clean_text(text: str) -> str:
    return " ".join(text.split()).strip()


def detect_opportunity_type(category: str, text: str) -> str:
    text_lower = text.lower()

    if "scholarship" in text_lower or category == "Scholarship":
        return "Scholarship"

    if "internship" in text_lower or category == "Internship":
        return "Internship"

    if "research" in text_lower:
        return "Research Opportunity"

    if "event" in text_lower or "seminar" in text_lower or "workshop" in text_lower:
        return "Event"

    if "career fair" in text_lower or "job fair" in text_lower:
        return "Career Opportunity"

    return category if category != "General" else "Unknown"


def extract_opportunity_details(html: str, category: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    text = clean_text(soup.get_text(" "))

    deadline_match = DEADLINE_PATTERN.search(text)
    deadline = deadline_match.group(2) if deadline_match else ""

    times = sorted(set(TIME_PATTERN.findall(text)))
    amounts = sorted(set(MONEY_PATTERN.findall(text)))

    opportunity_type = detect_opportunity_type(category, text)

    priority = "Normal"

    lower_text = text.lower()

    if deadline or "urgent" in lower_text or "apply now" in lower_text:
        priority = "High"

    if "deadline" in lower_text and ("scholarship" in lower_text or "internship" in lower_text):
        priority = "High"

    return {
        "Opportunity Type": opportunity_type,
        "Deadline": deadline,
        "Times Found": "; ".join(times),
        "Amounts Found": "; ".join(amounts),
        "Priority": priority,
    }