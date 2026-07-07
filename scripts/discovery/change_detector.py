"""
Change detection utilities for CoSE Pulse.

Compares the current crawl against the previous crawl snapshot.
"""

import csv
import hashlib
from pathlib import Path


def row_fingerprint(row: dict) -> str:
    important_fields = [
        row.get("URL", ""),
        row.get("Title", ""),
        row.get("Headings", ""),
        row.get("Summary", ""),
        row.get("Page Title", ""),
        row.get("H1", ""),
        row.get("Meta Description", ""),
        row.get("Category", ""),
        row.get("Opportunity Type", ""),
        row.get("Deadline", ""),
        row.get("Dates Found", ""),
    ]

    text = "||".join(important_fields)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_snapshot(snapshot_file: Path) -> dict:
    if not snapshot_file.exists():
        return {}

    with snapshot_file.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return {
            row["URL"]: row
            for row in reader
            if row.get("URL")
        }


def classify_changes(current_rows: list[dict], previous_rows: dict) -> list[dict]:
    changed_rows = []
    current_urls = set()

    for row in current_rows:
        url = row.get("URL", "")
        current_urls.add(url)

        current_hash = row_fingerprint(row)
        previous = previous_rows.get(url)

        if not previous:
            row["Change Status"] = "New"
        else:
            previous_hash = previous.get("Content Hash", "")

            if current_hash != previous_hash:
                row["Change Status"] = "Updated"
            else:
                row["Change Status"] = "Unchanged"

        row["Content Hash"] = current_hash
        changed_rows.append(row)

    for url, previous in previous_rows.items():
        if url not in current_urls:
            previous["Change Status"] = "Removed"
            changed_rows.append(previous)

    return changed_rows