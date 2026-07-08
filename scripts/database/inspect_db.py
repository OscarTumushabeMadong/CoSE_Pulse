"""
Inspect the CoSE Pulse SQLite database.
"""

from sqlite import get_connection


def main():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM discovered_pages")
    total_pages = cursor.fetchone()[0]

    cursor.execute("""
        SELECT category, COUNT(*)
        FROM discovered_pages
        GROUP BY category
        ORDER BY COUNT(*) DESC
    """)
    categories = cursor.fetchall()

    cursor.execute("""
        SELECT change_status, COUNT(*)
        FROM discovered_pages
        GROUP BY change_status
        ORDER BY COUNT(*) DESC
    """)
    changes = cursor.fetchall()

    print("=" * 60)
    print("CoSE Pulse Database Inspection")
    print("=" * 60)
    print(f"Total pages: {total_pages}")

    print("\nPages by category:")
    for category, count in categories:
        print(f"- {category}: {count}")

    print("\nPages by change status:")
    for status, count in changes:
        print(f"- {status}: {count}")

    connection.close()


if __name__ == "__main__":
    main()
