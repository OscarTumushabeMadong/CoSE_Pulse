"""
Builds structured output rows for discovered pages.

This module does not extract, classify, or score content.
It only assembles already-computed values into the final row format.
"""


def build_discovered_row(
    url: str,
    depth: int,
    status: str,
    department: str,
    category: str,
    classification_confidence: int,
    content: dict,
    metadata: dict,
    opportunity: dict,
    priority_score: int,
) -> dict:
    return {
        "URL": url,
        "Title": content["title"],
        "Headings": " | ".join(content["headings"]),
        "Summary": (content["paragraphs"][0][:300] if content["paragraphs"] else ""),
        "Page Title": metadata["Page Title"],
        "H1": metadata["H1"],
        "Meta Description": metadata["Meta Description"],
        "Canonical URL": metadata["Canonical URL"],
        "Depth": depth,
        "Status": status,
        "Department": department,
        "Category": category,
        "Classification Confidence": classification_confidence,
        "Emails Found": metadata["Emails Found"],
        "Phones Found": metadata["Phones Found"],
        "Dates Found": metadata["Dates Found"],
        "Opportunity Type": opportunity["Opportunity Type"],
        "Deadline": opportunity["Deadline"],
        "Times Found": opportunity["Times Found"],
        "Amounts Found": opportunity["Amounts Found"],
        "Priority": priority_score,
    }
