import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATABASE_DIR = PROJECT_ROOT / "scripts" / "database"
DISCOVERY_DIR = PROJECT_ROOT / "scripts" / "discovery"

if str(DISCOVERY_DIR) not in sys.path:
    sys.path.insert(0, str(DISCOVERY_DIR))

if str(DATABASE_DIR) not in sys.path:
    sys.path.insert(0, str(DATABASE_DIR))
    
from repository import (
    get_events,
    get_high_priority_pages,
    get_internships,
    get_new_pages,
    get_scholarships,
    get_updated_pages,
)

from crawl_engine import CrawlEngine
from pipeline import process_discovery_results

class DiscoveryService:

    def new_pages(self):
        return get_new_pages()

    def updated_pages(self):
        return get_updated_pages()

    def events(self):
        return get_events()

    def scholarships(self):
        return get_scholarships()

    def internships(self):
        return get_internships()

    def high_priority(self, minimum=70):
        return get_high_priority_pages(minimum)

    def run_discovery(self, output_file, snapshot_file):
        engine = CrawlEngine()
        rows = engine.run()

        rows_with_changes = process_discovery_results(
            rows=rows,
            output_file=output_file,
            snapshot_file=snapshot_file,
        )

        return rows_with_changes, engine.stats