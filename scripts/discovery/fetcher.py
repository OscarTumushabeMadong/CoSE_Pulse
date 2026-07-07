"""
HTTP fetching utilities for CoSE Pulse Discovery Engine.
"""

import sys
from pathlib import Path

import requests


PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from config.settings import TIMEOUT, USER_AGENT


def fetch_page(url: str) -> tuple[str, str]:
    headers = {
        "User-Agent": USER_AGENT
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=TIMEOUT
        )

        content_type = response.headers.get("Content-Type", "")

        if response.status_code >= 400:
            return "", f"HTTP {response.status_code}"

        if "text/html" not in content_type:
            return "", "Non-HTML"

        return response.text, "Success"

    except requests.exceptions.RequestException as error:
        return "", f"Request Error: {error}"