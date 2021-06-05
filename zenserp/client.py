from __future__ import annotations

from types import TracebackType
from typing import Any, Optional, Type

from requests import Response, Session

from .search import TBM, Device, SearchInput

STATUS_URL = "https://app.zenserp.com/api/v2/status"
SEARCH_URL = "https://app.zenserp.com/api/v2/search"


class Client:
    def __init__(self, api_key: str):
        if api_key == "":
            raise ValueError("no API key provided")
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

    def handle_error(self, response: Response) -> None:
        status_code = response.status_code
        if status_code == 200:
            return None
        elif status_code == 403:
            # TODO: Raise a custom exception about the HTTP status 403.
            message = response.json()["error"]
            raise Exception(message)
        elif status_code == 404:
            # TODO: Raise a custom exception about the HTTP status 404.
            response.raise_for_status()
        elif status_code == 500:
            # TODO: Raise a custom exception about the HTTP status 500.
            messages = response.json()["errors"].values()
            raise Exception(messages)
        else:
            response.raise_for_status()

    def status(self) -> int:
        """Checks the remaining requests of your API key.

        Returns:
            int: The remaining requests of your API key.
        """
        with self._session.get(STATUS_URL) as resp:
            resp.encoding = resp.apparent_encoding
            self.handle_error(resp)
            return resp.json()["remaining_requests"]

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
    ) -> Any:
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
        with self._session.get(SEARCH_URL, params=search_input.to_params()) as resp:
            resp.encoding = resp.apparent_encoding
            self.handle_error(resp)
            return resp.json()
