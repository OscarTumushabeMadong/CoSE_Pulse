"""
Pipeline orchestration helpers for CoSE Pulse Discovery Engine.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATABASE_DIR = PROJECT_ROOT / "scripts" / "database"

if str(DATABASE_DIR) not in sys.path:
    sys.path.insert(0, str(DATABASE_DIR))
    

from change_detector import classify_changes, load_snapshot
from exporter import save_discovered_pages
from repository import Repository


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