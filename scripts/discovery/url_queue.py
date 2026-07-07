"""
CoSE Pulse Discovery Engine

crawler.py

Discovers pages starting from the configured seed domains.
This module ONLY discovers pages. It does not parse contacts,
events, scholarships, or other content.
"""

import csv
import sys
import time
from collections import deque
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------
# Configure Python path
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = PROJECT_ROOT / "scripts"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

# ---------------------------------------------------------
# Project imports
# ---------------------------------------------------------

from config.settings import (
    MAX_DEPTH,
    MAX_PAGES,
    REQUEST_DELAY,
    SEED_DOMAINS,
    TIMEOUT,
    USER_AGENT,
)

from discovery.filters import normalize_url, should_crawl

# ---------------------------------------------------------
# Output directory
# ---------------------------------------------------------

OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

DISCOVERED_PAGES_FILE = OUTPUT_DIR / "discovered_pages.csv"

# ---------------------------------------------------------
# Download page
# ---------------------------------------------------------


def fetch_page(url: str) -> str:

    headers = {
        "User-Agent": USER_AGENT
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=TIMEOUT
    )

    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "")

    if "text/html" not in content_type:
        return ""

    return response.text


# ---------------------------------------------------------
# Extract internal links
# ---------------------------------------------------------


def extract_links(base_url: str, html: str) -> set[str]:

    soup = BeautifulSoup(html, "html.parser")

    discovered = set()

    for tag in soup.find_all("a", href=True):

        absolute = urljoin(base_url, tag["href"])

        absolute = normalize_url(absolute)

        if should_crawl(absolute):
            discovered.add(absolute)

    return discovered


# ---------------------------------------------------------
# Crawl
# ---------------------------------------------------------


def crawl() -> list[dict]:

    queue = deque()

    visited = set()

    discovered_rows = []

    for url in SEED_DOMAINS:
        queue.append((normalize_url(url), 0))

    while queue and len(visited) < MAX_PAGES:

        url, depth = queue.popleft()

        if url in visited:
            continue

        if depth > MAX_DEPTH:
            continue

        print(f"[Depth {depth}] {url}")

        visited.add(url)

        try:

            html = fetch_page(url)

        except Exception as e:

            print(f"ERROR: {url}")

            print(e)

            continue

        discovered_rows.append({

            "URL": url,

            "Depth": depth,

            "Status": "Discovered"

        })

        if html:

            links = extract_links(url, html)

            for link in sorted(links):

                if link not in visited:

                    queue.append((link, depth + 1))

        time.sleep(REQUEST_DELAY)

    return discovered_rows


# ---------------------------------------------------------
# Save CSV
# ---------------------------------------------------------


def save_csv(rows: list[dict]):

    with open(
        DISCOVERED_PAGES_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(

            file,

            fieldnames=[

                "URL",

                "Depth",

                "Status"

            ]

        )

        writer.writeheader()

        writer.writerows(rows)


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------


def main():

    print("=" * 60)
    print("CoSE Pulse Discovery Engine")
    print("=" * 60)

    rows = crawl()

    save_csv(rows)

    print()

    print("=" * 60)
    print(f"Pages discovered : {len(rows)}")
    print(f"Saved to         : {DISCOVERED_PAGES_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    main()