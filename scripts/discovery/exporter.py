"""
CSV export utilities for CoSE Pulse Discovery Engine.
"""

import csv


DISCOVERED_PAGE_FIELDNAMES = [
    "URL",
    "Title",
    "Headings",
    "Summary",

    "Page Title",
    "H1",
    "Meta Description",
    "Canonical URL",

    "Depth",
    "Status",
    "Department",
    "Category",
    "Classification Confidence",

    "Emails Found",
    "Phones Found",
    "Dates Found",

    "Opportunity Type",
    "Deadline",
    "Times Found",
    "Amounts Found",
    "Priority",
    
    "Change Status",
    "Content Hash",

]


def save_discovered_pages(file_path, rows: list[dict]) -> None:
    with open(
        file_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=DISCOVERED_PAGE_FIELDNAMES
        )

        writer.writeheader()
        writer.writerows(rows)