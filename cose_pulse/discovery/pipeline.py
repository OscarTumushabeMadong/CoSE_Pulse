"""
Pipeline orchestration helpers for CoSE Pulse Discovery Engine.
"""

from pathlib import Path

from cose_pulse.discovery.exporter import save_discovered_pages
from cose_pulse.discovery.change_detector import classify_changes, load_snapshot
from cose_pulse.database.repository import Repository


def process_discovery_results(
    rows: list[dict],
    output_file: Path,
    snapshot_file: Path,
) -> list[dict]:
    previous_rows = load_snapshot(snapshot_file)
    rows_with_changes = classify_changes(rows, previous_rows)

    save_discovered_pages(output_file, rows_with_changes)
    save_discovered_pages(snapshot_file, rows_with_changes)

    repository = Repository()
    repository.insert_many(rows_with_changes)

    return rows_with_changes
