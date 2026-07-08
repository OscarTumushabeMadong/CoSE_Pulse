"""
SQLite schema for CoSE Pulse.
"""

CREATE_DISCOVERED_PAGES_TABLE = """
CREATE TABLE IF NOT EXISTS discovered_pages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    url TEXT NOT NULL UNIQUE,
    title TEXT,
    headings TEXT,
    summary TEXT,

    page_title TEXT,
    h1 TEXT,
    meta_description TEXT,
    canonical_url TEXT,

    depth INTEGER,
    status TEXT,
    department TEXT,
    category TEXT,
    classification_confidence INTEGER,

    emails_found TEXT,
    phones_found TEXT,
    dates_found TEXT,

    opportunity_type TEXT,
    deadline TEXT,
    times_found TEXT,
    amounts_found TEXT,
    priority INTEGER,

    change_status TEXT,
    content_hash TEXT
);
"""

CREATE_TABLES = [
    CREATE_DISCOVERED_PAGES_TABLE,
]
