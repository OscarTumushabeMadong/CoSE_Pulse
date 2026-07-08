"""
Crawl Engine for CoSE Pulse Discovery Engine.

Owns the main crawl loop.
"""

import time
from crawl_scheduler import CrawlScheduler
from crawl_worker import CrawlWorker
from crawl_statistics import CrawlStatistics
from discovery_config import DiscoveryConfig

class CrawlEngine:
    def __init__(self, config: DiscoveryConfig = None):
        self.config = config or DiscoveryConfig()
        self.scheduler = CrawlScheduler(self.config)
        self.worker = CrawlWorker(self.config)
        self.stats = CrawlStatistics()

    def run(self) -> list[dict]:
        self.stats.start()
        
        discovered_rows = []

        while self.scheduler.has_next():
            url, depth = self.scheduler.next_url()

            if not url:
                continue

            print(f"[Depth {depth}] {url}")

            result = self.worker.process(url, depth)

            discovered_rows.append(result.row)

            self.stats.pages_processed += 1

            if result.row["Status"] == "Success":
                self.stats.successful_pages += 1
            else:
                self.stats.failed_pages += 1

            self.scheduler.add_links(result.links, depth)

            self.stats.links_discovered += len(result.links)

            time.sleep(self.config.request_delay)

            self.stats.stop()

        return discovered_rows