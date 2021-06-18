from __future__ import annotations

from types import TracebackType
from typing import Mapping, Optional, Type, cast

from requests import Response, Session

from .exceptions import status_handler
from .search import SERP, TBM, Device, SearchInput
from .status import Status

STATUS_URL = "https://app.zenserp.com/api/v2/status"
SEARCH_URL = "https://app.zenserp.com/api/v2/search"


class Client:
    def __init__(self, api_key: str) -> None:
        """The client to request Zenserp.

        Args:
            api_key (str): Your API key of Zenserp.
        """
        self._session = Session()
        self._session.headers["apikey"] = api_key

    def __enter__(self) -> Client:
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        return self.close()

    def close(self) -> None:
        """Closes this client."""
        return self._session.close()

    @status_handler
    def _get(self, url: str, params: Optional[Mapping[str, str]] = None) -> Response:
        with self._session.get(url, params=params) as resp:
            resp.encoding = resp.apparent_encoding
            return resp

    def status(self) -> Status:
        """Checks the status of your API key.

        Returns:
            The status of your API key.
        """
        with self._get(STATUS_URL) as resp:
            return Status(resp.json()["remaining_requests"])

    def search(
        self,
        query: str,
        location: Optional[str] = None,
        search_engine: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        tbm: Optional[TBM] = None,
        device: Optional[Device] = None,
        timeframe: Optional[str] = None,
        gl: Optional[str] = None,
        lr: Optional[str] = None,
        hl: Optional[str] = None,
        latitude: Optional[str] = None,
        longitude: Optional[str] = None,
    ) -> SERP:
        """Google Search.

        Args:
            query: A keyword to query.
            location: A geolocation used in the query.
            search_engine: A URL of the search engine to query.
            limit: A number of search results. It can be 1 - 100.
            offset: An offset for the search results.
            tbm: A type of the Google Search.
            device: A device to use for the Google Search.
            timeframe: Time interval of you interests.
            gl:
                A country code that means the country to use for the Google Search.
                It is automatically detected from the 'search_engine' if not supplied.
            lr:
                One or multiple country codes that limits languages the Google Search.
                It is automatically detected from the 'search_engine' if not supplied.
            hl:
                A language code that means the language to use for the Google Search.
                It is automatically detected from the 'search_engine' if not supplied.
            latitude: A latitude of a geolocation used in the query.
            longitude: A longitude of a geolocation used in the query.

        Returns:
            Search results from the search via Zenserp.
        """
        search_input = SearchInput(
            query,
            location=location,
            search_engine=search_engine,
            limit=limit,
            offset=offset,
            tbm=tbm,
            device=device,
            timeframe=timeframe,
            gl=gl,
            lr=lr,
            hl=hl,
            latitude=latitude,
            longitude=longitude,
        )
        with self._get(SEARCH_URL, params=search_input.to_params()) as resp:
            return cast(SERP, resp.json())
