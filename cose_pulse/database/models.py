"""
Shared data models for CoSE Pulse.
"""

from dataclasses import dataclass


@dataclass
class FetchResult:
    url: str
    status: str
    html: str
    response_time: float = 0.0
    error: str = ""


@dataclass
class ProcessResult:
    row: dict
    links: list[str]


@dataclass
class DiscoveryResult:
    rows: list[dict]
    rows_with_changes: list[dict]
    stats: object
