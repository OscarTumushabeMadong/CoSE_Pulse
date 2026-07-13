"""
Basic verification script for DiscoveryService.
"""

from cose_pulse.database.database import Database
from cose_pulse.database.repository import Repository
from cose_pulse.services.discovery_service import DiscoveryService


def main() -> None:
    database = Database()
    repository = Repository(database)
    service = DiscoveryService(repository)

    print()
    print("New")
    print(len(service.new_pages()))

    print()
    print("Events")
    print(len(service.events()))

    print()
    print("High Priority")
    print(len(service.high_priority()))


if __name__ == "__main__":
    main()
