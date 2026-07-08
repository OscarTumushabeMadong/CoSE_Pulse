"""
Database repository functions for CoSE Pulse.
"""

from sqlite import get_connection


def insert_page(row: dict):
    """
    Insert one discovered page into SQLite.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO discovered_pages
        (
            url,
            title,
            headings,
            summary,

            page_title,
            h1,
            meta_description,
            canonical_url,

            depth,
            status,
            department,
            category,
            classification_confidence,

            emails_found,
            phones_found,
            dates_found,

            opportunity_type,
            deadline,
            times_found,
            amounts_found,
            priority,

            change_status,
            content_hash
        )
        VALUES 
        (
            ?,?,?,?,?,?,
            ?,?,?,?,?,?,
            ?,?,?,?,?,?,
            ?,?,?,?,?
        )
        """,
        (
            row["URL"],
            row["Title"],
            row["Headings"],
            row["Summary"],

            row["Page Title"],
            row["H1"],
            row["Meta Description"],
            row["Canonical URL"],

            row["Depth"],
            row["Status"],
            row["Department"],
            row["Category"],
            row["Classification Confidence"],

            row["Emails Found"],
            row["Phones Found"],
            row["Dates Found"],

            row["Opportunity Type"],
            row["Deadline"],
            row["Times Found"],
            row["Amounts Found"],
            row["Priority"],

            row["Change Status"],
            row["Content Hash"],
        ),
    )

    connection.commit()
    connection.close()


def insert_many(rows):

    for row in rows:
        insert_page(row)

def fetch_all(query: str, params: tuple = ()):
    connection = get_connection()
    connection.row_factory = lambda cursor, row: {
        col[0]: row[idx]
        for idx, col in enumerate(cursor.description)
    }

    cursor = connection.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()

    connection.close()
    return rows


def get_new_pages():
    return fetch_all("""
        SELECT *
        FROM discovered_pages
        WHERE change_status = 'New'
        ORDER BY priority DESC
    """)


def get_updated_pages():
    return fetch_all("""
        SELECT *
        FROM discovered_pages
        WHERE change_status = 'Updated'
        ORDER BY priority DESC
    """)


def get_events():
    return fetch_all("""
        SELECT *
        FROM discovered_pages
        WHERE category = 'Event'
        ORDER BY priority DESC
    """)


def get_scholarships():
    return fetch_all("""
        SELECT *
        FROM discovered_pages
        WHERE category = 'Scholarship'
           OR opportunity_type = 'Scholarship'
        ORDER BY priority DESC
    """)


def get_internships():
    return fetch_all("""
        SELECT *
        FROM discovered_pages
        WHERE category = 'Internship'
           OR opportunity_type = 'Internship'
        ORDER BY priority DESC
    """)


def get_high_priority_pages(min_priority: int = 70):
    return fetch_all("""
        SELECT *
        FROM discovered_pages
        WHERE priority >= ?
        ORDER BY priority DESC
    """, (min_priority,))