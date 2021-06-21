from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterable, Optional, Union

SERP = dict[str, Any]
HL = Iterable[dict[str, str]]
GL = Iterable[dict[str, str]]
Locations = Iterable[str]
SearchEngines = Iterable[str]


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
class SearchInput:
    """Parameters for Google Search."""

    query: str
    location: Optional[str] = None
    search_engine: Optional[str] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    tbm: Optional[TBM] = None
    device: Optional[Device] = None
    timeframe: Optional[str] = None
    gl: Optional[str] = None
    lr: Optional[str] = None
    hl: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None

    def to_params(self) -> dict[str, Union[str, int]]:
        """Converts to query parameters for the 'search' endpoint of Zenserp.

        Returns:
            Query parameters for the 'search' endpoint of Zenserp.
        """
        return {
            k: v
            for k, v in {
                "q": self.query,
                "location": self.location,
                "search_engine": self.search_engine,
                "num": self.limit,
                "start": self.offset,
                "tbm": None if self.tbm is None else self.tbm.value,
                "device": None if self.device is None else self.device.value,
                "timeframe": self.timeframe,
                "gl": self.gl,
                "lr": self.lr,
                "hl": self.hl,
                "lat": self.latitude,
                "lng": self.longitude,
            }.items()
            if v is not None
        }
