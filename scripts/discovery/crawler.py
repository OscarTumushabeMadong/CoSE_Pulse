"""
CoSE Pulse Discovery Engine

crawler.py

Discovers pages starting from the configured seed domains.
This module ONLY discovers pages. It does not parse contacts,
events, scholarships, or other content.
"""

import sys
from pathlib import Path




# ---------------------------------------------------------
# Configure Python path
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
SERVICES_DIR = PROJECT_ROOT / "scripts" / "services"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

if str(SERVICES_DIR) not in sys.path:
    sys.path.insert(0, str(SERVICES_DIR))

from discovery_service import DiscoveryService
from pipeline import process_discovery_results

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
    engine = CrawlEngine()
    return engine.run()
    

# ---------------------------------------------------------
# Main
# ---------------------------------------------------------


def main():
    print("=" * 60)
    print("CoSE Pulse Discovery Engine")
    print("=" * 60)

    service = DiscoveryService()

    rows_with_changes, stats = service.run_discovery(
        output_file=DISCOVERED_PAGES_FILE,
        snapshot_file=SNAPSHOT_FILE,
    )

    print(f"Pages processed : {stats.pages_processed}")
    print(f"Successful pages : {stats.successful_pages}")
    print(f"Failed pages     : {stats.failed_pages}")
    print(f"Links discovered : {stats.links_discovered}")
    print(f"Elapsed seconds  : {stats.elapsed:.2f}")

    print()
    print(f"Saved CSV       : {DISCOVERED_PAGES_FILE}")
    print("Saved to SQLite : Success")
    print("=" * 60)


if __name__ == "__main__":
    main()