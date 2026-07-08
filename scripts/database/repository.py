"""
Database repository for CoSE Pulse.
"""

from database import Database


class Repository:
    def __init__(self, database=None):
        self.database = database or Database()

    def insert_page(self, row: dict):
        self.database.execute(
            """
            INSERT OR REPLACE INTO discovered_pages
            (
                url, title, headings, summary,
                page_title, h1, meta_description, canonical_url,
                depth, status, department, category, classification_confidence,
                emails_found, phones_found, dates_found,
                opportunity_type, deadline, times_found, amounts_found, priority,
                change_status, content_hash
            )
            VALUES
            (
                ?, ?, ?, ?,
                ?, ?, ?, ?,
                ?, ?, ?, ?, ?,
                ?, ?, ?,
                ?, ?, ?, ?, ?,
                ?, ?
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

    def insert_many(self, rows):
        for row in rows:
            self.insert_page(row)

    def fetch_all(self, query: str, params: tuple = ()):
        return self.database.fetch_all(query, params)

    def get_new_pages(self):
        return self.fetch_all("""
            SELECT *
            FROM discovered_pages
            WHERE change_status = 'New'
            ORDER BY priority DESC
        """)

    def get_updated_pages(self):
        return self.fetch_all("""
            SELECT *
            FROM discovered_pages
            WHERE change_status = 'Updated'
            ORDER BY priority DESC
        """)

    def get_events(self):
        return self.fetch_all("""
            SELECT *
            FROM discovered_pages
            WHERE category = 'Event'
            ORDER BY priority DESC
        """)

    def get_scholarships(self):
        return self.fetch_all("""
            SELECT *
            FROM discovered_pages
            WHERE category = 'Scholarship'
               OR opportunity_type = 'Scholarship'
            ORDER BY priority DESC
        """)

    def get_internships(self):
        return self.fetch_all("""
            SELECT *
            FROM discovered_pages
            WHERE category = 'Internship'
               OR opportunity_type = 'Internship'
            ORDER BY priority DESC
        """)

    def get_high_priority_pages(self, min_priority: int = 70):
        return self.fetch_all(
            """
            SELECT *
            FROM discovered_pages
            WHERE priority >= ?
            ORDER BY priority DESC
            """,
            (min_priority,),
        )