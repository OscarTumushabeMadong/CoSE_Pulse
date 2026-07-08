import time
import sys
from pathlib import Path
import requests

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATABASE_DIR = PROJECT_ROOT / "scripts" / "database"

if str(DATABASE_DIR) not in sys.path:
    sys.path.insert(0, str(DATABASE_DIR))

from models import FetchResult


def fetch_page(url: str, config) -> FetchResult:
    headers = {"User-Agent": config.user_agent}

    start = time.perf_counter()

    try:
        response = requests.get(url, headers=headers, timeout=config.timeout)

        elapsed = time.perf_counter() - start

        if response.status_code != 200:
            return FetchResult(
                url=url,
                status=f"HTTP {response.status_code}",
                html="",
                response_time=elapsed,
                error=response.reason,
            )

        return FetchResult(
            url=url,
            status="Success",
            html=response.text,
            response_time=elapsed,
        )

    except requests.RequestException as error:
        elapsed = time.perf_counter() - start

        return FetchResult(
            url=url,
            status="Request Error",
            html="",
            response_time=elapsed,
            error=str(error),
        )
