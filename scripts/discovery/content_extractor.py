"""
Extract structured content from HTML pages.
"""

from bs4 import BeautifulSoup


def extract_page_content(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    title = ""

    if soup.title:
        title = soup.title.get_text(strip=True)

    headings = []

    for tag in soup.find_all(["h1", "h2"]):
        text = tag.get_text(" ", strip=True)

        if text:
            headings.append(text)

    paragraphs = []

    for p in soup.find_all("p"):
        text = p.get_text(" ", strip=True)

        if len(text) > 40:
            paragraphs.append(text)

    return {
        "title": title,
        "headings": headings,
        "paragraphs": paragraphs,
    }
