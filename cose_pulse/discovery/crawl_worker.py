"""
Processes a single page during crawling.
"""

from cose_pulse.discovery.fetcher import fetch_page
from cose_pulse.discovery.link_extractor import extract_links
from cose_pulse.discovery.page_processor import process_page
from cose_pulse.database.models import ProcessResult


class CrawlWorker:
    def __init__(self, config):
        self.config = config

    def process(self, url, depth):
        fetch_result = fetch_page(url, self.config)

        if fetch_result.status != "Success":
            print(f"{fetch_result.status} for {url}")

        row = process_page(
            url=url,
            depth=depth,
            status=fetch_result.status,
            html=fetch_result.html,
        )

        links = []

        if fetch_result.html:
            links = extract_links(url, fetch_result.html)

        return ProcessResult(row=row, links=links)
