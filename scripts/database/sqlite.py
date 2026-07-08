"""
SQLite connection and initialization utilities for CoSE Pulse.
"""

import sqlite3
from pathlib import Path

from schema import CREATE_TABLES


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

DATABASE_FILE = DATA_DIR / "cose_pulse.db"


def get_connection():
    return sqlite3.connect(DATABASE_FILE)


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    for statement in CREATE_TABLES:
        cursor.execute(statement)

    connection.commit()
    connection.close()

    print(f"Database initialized: {DATABASE_FILE}")


if __name__ == "__main__":
    initialize_database()
