# SFSU CoSE Contact Scraper

An automated Python-based data collection system that extracts, validates, normalizes, and exports faculty and staff contact information from San Francisco State University's College of Science & Engineering and related academic departments.

---

## Overview

The purpose of this project is to build a high-quality institutional contact database by automatically scraping official SFSU websites.

Instead of manually copying hundreds of contacts, the scraper:

- Crawls department websites
- Extracts contact information
- Cleans inconsistent formatting
- Scores data quality
- Separates clean records from those needing review
- Produces CSV files ready for Excel, LibreOffice, or databases

---

## Current Features

### Website Crawling

Currently supports scraping:

- College of Science & Engineering
- School of Engineering
- Computer Science
- Mathematics
- Physics & Astronomy
- Chemistry & Biochemistry
- Psychology

Additional departments can be added through modular parsers.

---

## Data Extracted

Each contact includes, when available:

- Department
- Category
- Contact Type
- Quality
- Confidence Score
- First Name
- Last Name
- Title
- Email
- Generic Email Flag
- Phone
- Office
- Source URL
- Date Collected
- Notes

---

## Project Structure

```
SFSU_CoSE_Scraper/

config/
data/
docs/
logs/
output/

scripts/
    sfsu_cose_contacts_scraper.py

    parsers/
        common.py
        engineering.py
        psychology.py
        validator.py
        normalizer.py
        change_detector.py

README.md
.gitignore
```

---

## Workflow

```
Website

↓

HTML Download

↓

Department Parser

↓

Validation

↓

Normalization

↓

Confidence Scoring

↓

CSV Export
```

---

## Output Files

The scraper generates three datasets.

### Raw

Contains every extracted contact.

```
sfsu_cose_contacts_raw.csv
```

---

### Review

Contains contacts needing manual inspection.

Examples:

- Missing names
- Missing titles
- Generic department email
- Low confidence extraction

```
sfsu_cose_contacts_review.csv
```

---

### Clean

Contains only high-confidence contacts suitable for production use.

```
sfsu_cose_contacts_clean.csv
```

---

## Technologies

- Python 3.13
- Requests
- BeautifulSoup4
- CSV
- Git
- GitHub

---

## Running

Install dependencies:

```bash
pip install requests beautifulsoup4 pandas
```

Run:

```bash
python3 scripts/sfsu_cose_contacts_scraper.py
```

---

## Current Status

Version 1.0

Completed:

- Modular parser architecture
- Validation engine
- Name normalization
- Confidence scoring
- Multiple CSV outputs
- Git version control
- GitHub repository

---

## Planned Features

### Version 2

- Automatic pagination
- Recursive crawling
- Department auto-discovery
- Better faculty profile parsing
- Duplicate detection
- Change detection between scraper runs

### Version 3

- SQLite database
- Excel export
- REST API
- Web dashboard
- Search interface

### Version 4

- Microsoft Graph integration
- Automated email generation
- CRM synchronization

---

## Author

Oscar Tumushabe Madong

Computer Engineering

San Francisco State University