import csv
from pathlib import Path


KEY_FIELD = "Email"


def load_previous_snapshot(snapshot_file: Path) -> dict:
    if not snapshot_file.exists():
        return {}

    with snapshot_file.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return {row[KEY_FIELD].lower(): row for row in reader if row.get(KEY_FIELD)}


def detect_changes(current_rows: list[dict], previous_rows: dict) -> list[dict]:
    current_by_email = {
        row[KEY_FIELD].lower(): row for row in current_rows if row.get(KEY_FIELD)
    }

    results = []

    for email, row in current_by_email.items():
        previous = previous_rows.get(email)

        if not previous:
            row["Change Status"] = "New"
            results.append(row)
            continue

        changed_fields = []

        for field in ["Name", "Title", "Phone", "Office", "Department", "Category"]:
            if row.get(field, "") != previous.get(field, ""):
                changed_fields.append(field)

        if changed_fields:
            row["Change Status"] = "Updated"
            row["Notes"] = (
                row.get("Notes", "") + f" Changed fields: {', '.join(changed_fields)}."
            ).strip()
        else:
            row["Change Status"] = "Unchanged"

        results.append(row)

    previous_emails = set(previous_rows.keys())
    current_emails = set(current_by_email.keys())

    removed_emails = previous_emails - current_emails

    for email in removed_emails:
        removed_row = previous_rows[email]
        removed_row["Change Status"] = "Removed"
        results.append(removed_row)

    return results
