"""
Statistics collector for the CoSE Pulse Discovery Engine.
"""

from dataclasses import dataclass
import time


@dataclass
class CrawlStatistics:
    pages_processed: int = 0
    successful_pages: int = 0
    failed_pages: int = 0

    links_discovered: int = 0

    start_time: float = 0.0
    end_time: float = 0.0

    def start(self):
        self.start_time = time.perf_counter()

    def stop(self):
        self.end_time = time.perf_counter()

    @property
    def elapsed(self):
        return self.end_time - self.start_time
