"""
Crawl scheduling utilities for CoSE Pulse Discovery Engine.

Responsible for queue management, visited tracking, depth limits,
and page-count limits.
"""

from collections import deque

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
    

from filters import normalize_url


class CrawlScheduler:
    def __init__(self, config):
        self.config = config
        self.queue = deque()
        self.visited = set()

        for seed in self.config.seed_domains:
            self.add_url(seed, depth=0)

    def add_url(self, url: str, depth: int):
        url = normalize_url(url)

        if not url:
            return

        if url in self.visited:
            return

        if depth > self.config.max_depth:
            return

        self.queue.append((url, depth))

    def has_next(self) -> bool:
        return bool(self.queue) and len(self.visited) < self.config.max_pages

    def next_url(self):
        url, depth = self.queue.popleft()

        if url in self.visited:
            return None, None

        self.visited.add(url)

        return url, depth

    def add_links(self, links, current_depth: int):
        for link in sorted(links):
            self.add_url(link, current_depth + 1)

    def visited_count(self) -> int:
        return len(self.visited)