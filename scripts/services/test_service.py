import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATABASE_DIR = PROJECT_ROOT / "scripts" / "database"

if str(DATABASE_DIR) not in sys.path:
    sys.path.insert(0, str(DATABASE_DIR))

from database import Database
from repository import Repository
from discovery_service import DiscoveryService


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