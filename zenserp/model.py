from dataclasses import dataclass
from enum import Enum
from typing import Any


class TBM(Enum):
    """Types of the Google Search."""

    IMAGE_SEARCH = "isch"
    VIDEO_SEARCH = "vid"
    MAPS_SEARCH = "lcl"
    NEWS_SEARCH = "nws"
    SHOPPING_SEARCH = "shop"


class Device(Enum):
    """Devices used for the Google Search."""

    DESKTOP = "desktop"
    MOBILE = "mobile"


@dataclass(frozen=True)
class Status:
    """The status or your API key."""

    remaining_requests: int


SERP = dict[str, Any]
"""Search results from the search via Zenserp."""


@dataclass(frozen=True)
class HL:
    """A language code that means the language to use for the Google Search."""

    code: str
    name: str


@dataclass(frozen=True)
class GL:
    """A country code that means the country to use for the Google Search."""

    code: str
    name: str


Location = str
"""A geolocation used in the query."""

SearchEngine = str
"""A URL of the search engine to query."""
