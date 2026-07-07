"""
Metadata extraction utilities for CoSE Pulse Discovery Engine.
"""

import re
from bs4 import BeautifulSoup


EMAIL_PATTERN = re.compile(
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
)

PHONE_PATTERN = re.compile(
    r"(?:\+1\s*)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}"
)

DATE_PATTERN = re.compile(
    r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)"
    r"[a-z]*\.?\s+\d{1,2},?\s+\d{4}\b",
    re.IGNORECASE,
)


def clean_text(text: str) -> str:
    return " ".join(text.split()).strip()


def extract_metadata(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    page_text = clean_text(soup.get_text(" "))

    title = ""
    if soup.title:
        title = clean_text(soup.title.get_text(" "))

    h1 = ""
    h1_tag = soup.find("h1")
    if h1_tag:
        h1 = clean_text(h1_tag.get_text(" "))

    meta_description = ""
    meta_tag = soup.find("meta", attrs={"name": "description"})
    if meta_tag and meta_tag.get("content"):
        meta_description = clean_text(meta_tag["content"])

    canonical_url = ""
    canonical_tag = soup.find("link", rel="canonical")
    if canonical_tag and canonical_tag.get("href"):
        canonical_url = canonical_tag["href"].strip()

    emails = sorted(set(EMAIL_PATTERN.findall(page_text)))
    phones = sorted(set(PHONE_PATTERN.findall(page_text)))
    dates = sorted(set(DATE_PATTERN.findall(page_text)))

    return {
        "Page Title": title,
        "H1": h1,
        "Meta Description": meta_description,
        "Canonical URL": canonical_url,
        "Emails Found": "; ".join(emails),
        "Phones Found": "; ".join(phones),
        "Dates Found": "; ".join(dates),
    }