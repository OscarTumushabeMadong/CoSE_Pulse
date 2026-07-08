"""
Configuration object for the CoSE Pulse Discovery Engine.
"""

from dataclasses import dataclass, field

from config.settings import (
    MAX_DEPTH,
    MAX_PAGES,
    REQUEST_DELAY,
    SEED_DOMAINS,
    TIMEOUT,
    USER_AGENT,
)


@dataclass
class DiscoveryConfig:
    seed_domains: list[str] = field(default_factory=lambda: list(SEED_DOMAINS))
    max_depth: int = MAX_DEPTH
    max_pages: int = MAX_PAGES
    request_delay: float = REQUEST_DELAY
    timeout: int = TIMEOUT
    user_agent: str = USER_AGENT
