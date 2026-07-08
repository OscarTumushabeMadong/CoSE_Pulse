"""
Shared data models for CoSE Pulse.
"""

from dataclasses import dataclass
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