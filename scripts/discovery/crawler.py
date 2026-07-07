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


import requests


from fetcher import fetch_page

from link_extractor import extract_links

from pipeline import process_discovery_results

from page_processor import process_page

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

from filters import normalize_url, should_crawl

# ---------------------------------------------------------
# Output directory
# ---------------------------------------------------------

OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

DISCOVERED_PAGES_FILE = OUTPUT_DIR / "discovered_pages.csv"

SNAPSHOT_FILE = OUTPUT_DIR / "snapshot.csv"


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

        html, status = fetch_page(url)
        
        
        if status != "Success":
            print(f"{status} for {url}")

        
        row = process_page(
            url=url, 
            depth=depth, 
            status=status, 
            html=html,
        )
        
        discovered_rows.append(row)

        if html:

            links = extract_links(url, html)

            for link in sorted(links):

                if link not in visited:

                    queue.append((link, depth + 1))

        time.sleep(REQUEST_DELAY)

    return discovered_rows

# ---------------------------------------------------------
# Main
# ---------------------------------------------------------


def main():
    print("=" * 60)
    print("CoSE Pulse Discovery Engine")
    print("=" * 60)

    rows = crawl()
    
    rows_with_changes = process_discovery_results(
        rows=rows,
        output_file=DISCOVERED_PAGES_FILE,
        snapshot_file=SNAPSHOT_FILE,
    )

    print()
    print("=" * 60)
    print(f"Pages processed : {len(rows)}")
    print(f"Saved to        : {DISCOVERED_PAGES_FILE}")
    print("Saved to SQLite : Success")
    print("=" * 60)


if __name__ == "__main__":
    main()