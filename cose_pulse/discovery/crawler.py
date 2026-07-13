"""
CoSE Pulse Discovery Engine entry point.
"""

from cose_pulse.services.discovery_service import DiscoveryService


# ------------------------------------------------------------
# Configure Python path
# ------------------------------------------------------------


from cose_pulse.database.database import Database
from cose_pulse.database.repository import Repository


# ------------------------------------------------------------
# Output paths
# ------------------------------------------------------------
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

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
