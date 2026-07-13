"""
Link extraction utilities for CoSE Pulse Discovery Engine.
"""

from urllib.parse import urljoin

from bs4 import BeautifulSoup

from cose_pulse.discovery.filters import normalize_url, should_crawl


def extract_links(base_url: str, html: str) -> set[str]:
    soup = BeautifulSoup(html, "html.parser")
    links = set()

    for tag in soup.find_all("a", href=True):
        absolute_url = urljoin(base_url, tag["href"])
        absolute_url = normalize_url(absolute_url)

        if should_crawl(absolute_url):
            links.add(absolute_url)

    return links
