from urllib.parse import urlparse

from config.settings import ALLOWED_DOMAINS, IGNORE_EXTENSIONS


def normalize_url(url: str) -> str:
    url = url.strip()

    if "#" in url:
        url = url.split("#", 1)[0]

    if url.endswith("/"):
        url = url[:-1]

    return url


def is_allowed_domain(url: str) -> bool:
    domain = urlparse(url).netloc.lower()
    return domain in ALLOWED_DOMAINS


def has_ignored_extension(url: str) -> bool:
    path = urlparse(url).path.lower()
    return any(path.endswith(ext) for ext in IGNORE_EXTENSIONS)


def should_crawl(url: str) -> bool:
    if not url:
        return False

    if not url.startswith(("http://", "https://")):
        return False

    if not is_allowed_domain(url):
        return False

    if has_ignored_extension(url):
        return False

    return True
