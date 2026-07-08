"""
CoSE Pulse Discovery Engine entry point.
"""

import sys
from pathlib import Path


# ------------------------------------------------------------
# Configure Python path
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SCRIPTS_DIR = PROJECT_ROOT / "scripts"
SERVICES_DIR = PROJECT_ROOT / "scripts" / "services"
DATABASE_DIR = PROJECT_ROOT / "scripts" / "database"

for path in [PROJECT_ROOT, SCRIPTS_DIR, SERVICES_DIR, DATABASE_DIR]:
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))


from database import Database
from repository import Repository
from discovery_service import DiscoveryService


# ------------------------------------------------------------
# Output paths
# ------------------------------------------------------------

OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

DISCOVERED_PAGES_FILE = OUTPUT_DIR / "discovered_pages.csv"
SNAPSHOT_FILE = OUTPUT_DIR / "snapshot.csv"


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------


def main():
    print("=" * 60)
    print("CoSE Pulse Discovery Engine")
    print("=" * 60)

    database = Database()
    repository = Repository(database)
    service = DiscoveryService(repository)

    result = service.run_discovery(
        output_file=DISCOVERED_PAGES_FILE,
        snapshot_file=SNAPSHOT_FILE,
    )

    stats = result.stats

    print()
    print("=" * 60)
    print("Crawl Summary")
    print("=" * 60)
    print(f"Pages processed : {stats.pages_processed}")
    print(f"Successful pages: {stats.successful_pages}")
    print(f"Failed pages    : {stats.failed_pages}")
    print(f"Links discovered: {stats.links_discovered}")
    print(f"Elapsed seconds : {stats.elapsed:.2f}")
    print()
    print(f"Saved CSV       : {DISCOVERED_PAGES_FILE}")
    print("Saved to SQLite : Success")
    print("=" * 60)


if __name__ == "__main__":
    main()
