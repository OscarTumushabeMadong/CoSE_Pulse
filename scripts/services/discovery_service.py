import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATABASE_DIR = PROJECT_ROOT / "scripts" / "database"
DISCOVERY_DIR = PROJECT_ROOT / "scripts" / "discovery"

if str(DATABASE_DIR) not in sys.path:
    sys.path.insert(0, str(DATABASE_DIR))

if str(DISCOVERY_DIR) not in sys.path:
    sys.path.insert(0, str(DISCOVERY_DIR))

from models import DiscoveryResult
from crawl_engine import CrawlEngine
from pipeline import process_discovery_results
from repository import Repository


class DiscoveryService:
    def __init__(self, repository: Repository):
        self.repository = repository

    def new_pages(self):
        return self.repository.get_new_pages()

    def updated_pages(self):
        return self.repository.get_updated_pages()

    def events(self):
        return self.repository.get_events()

    def scholarships(self):
        return self.repository.get_scholarships()

    def internships(self):
        return self.repository.get_internships()

    def high_priority(self, minimum=70):
        return self.repository.get_high_priority_pages(minimum)

    def run_discovery(self, output_file, snapshot_file):
        engine = CrawlEngine()
        rows = engine.run()

        rows_with_changes = process_discovery_results(
            rows=rows,
            output_file=output_file,
            snapshot_file=snapshot_file,
        )

        return DiscoveryResult(
            rows=rows,
            rows_with_changes=rows_with_changes,
            stats=engine.stats,
        )
