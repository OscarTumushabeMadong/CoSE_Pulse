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

CREATE_CATEGORY_INDEX = """
CREATE INDEX IF NOT EXISTS idx_discovered_pages_category
ON discovered_pages(category);
"""

CREATE_DEPARTMENT_INDEX = """
CREATE INDEX IF NOT EXISTS idx_discovered_pages_department
ON discovered_pages(department);
"""

CREATE_PRIORITY_INDEX = """
CREATE INDEX IF NOT EXISTS idx_discovered_pages_priority
ON discovered_pages(priority);
"""

CREATE_CHANGE_STATUS_INDEX = """
CREATE INDEX IF NOT EXISTS idx_discovered_pages_change_status
ON discovered_pages(change_status);
"""

CREATE_TABLES = [
    CREATE_DISCOVERED_PAGES_TABLE,
    CREATE_CATEGORY_INDEX,
    CREATE_DEPARTMENT_INDEX,
    CREATE_PRIORITY_INDEX,
    CREATE_CHANGE_STATUS_INDEX,
]
