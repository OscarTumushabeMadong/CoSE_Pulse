"""
Application service for CoSE Pulse discovery operations.

This service coordinates the crawl engine, discovery pipeline,
and repository query operations.
"""

from pathlib import Path

from cose_pulse.database.models import DiscoveryResult
from cose_pulse.database.repository import Repository
from cose_pulse.discovery.crawl_engine import CrawlEngine
from cose_pulse.discovery.pipeline import process_discovery_results


class DiscoveryService:
    """
    Coordinates discovery execution and access to stored discovery results.
    """

    def __init__(self, repository: Repository) -> None:
        self.repository = repository

    def new_pages(self) -> list[dict]:
        return self.repository.get_new_pages()

    def updated_pages(self) -> list[dict]:
        return self.repository.get_updated_pages()

    def events(self) -> list[dict]:
        return self.repository.get_events()

    def scholarships(self) -> list[dict]:
        return self.repository.get_scholarships()

    def internships(self) -> list[dict]:
        return self.repository.get_internships()

    def high_priority(self, minimum: int = 70) -> list[dict]:
        return self.repository.get_high_priority_pages(minimum)

    def run_discovery(
        self,
        output_file: Path,
        snapshot_file: Path,
    ) -> DiscoveryResult:
        """
        Run the crawler, process detected changes, export results,
        and return the complete discovery result.
        """

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
