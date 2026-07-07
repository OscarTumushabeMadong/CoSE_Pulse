"""
Page processing utilities for CoSE Pulse Discovery Engine.

This module turns one fetched page into one structured row by running
classification, content extraction, metadata extraction, opportunity
extraction, and priority scoring.
"""

from classifier import classify_url, get_department
from content_extractor import extract_page_content
from metadata import extract_metadata
from opportunity_extractor import extract_opportunity_details
from prioritizer import calculate_priority
from row_builder import build_discovered_row


def process_page(
    url: str,
    depth: int,
    status: str,
    html: str,
) -> dict:
    category, classification_confidence = classify_url(url)

    content = extract_page_content(html) if html else {
        "title": "",
        "headings": [],
        "paragraphs": [],
    }

    metadata = extract_metadata(html) if html else {
        "Page Title": "",
        "H1": "",
        "Meta Description": "",
        "Canonical URL": "",
        "Emails Found": "",
        "Phones Found": "",
        "Dates Found": "",
    }

    opportunity = extract_opportunity_details(html, category) if html else {
        "Opportunity Type": "",
        "Deadline": "",
        "Times Found": "",
        "Amounts Found": "",
        "Priority": "",
    }

    priority_score = calculate_priority({
        "Category": category,
        "Opportunity Type": opportunity["Opportunity Type"],
        "Deadline": opportunity["Deadline"],
    })

    return build_discovered_row(
        url=url,
        depth=depth,
        status=status,
        department=get_department(url),
        category=category,
        classification_confidence=classification_confidence,
        content=content,
        metadata=metadata,
        opportunity=opportunity,
        priority_score=priority_score,
    )