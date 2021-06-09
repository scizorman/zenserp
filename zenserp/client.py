from __future__ import annotations

from types import TracebackType
from typing import Optional, Type, cast

from requests import Response, Session

from .search import SERP, TBM, Device, SearchInput
from .status import Status

STATUS_URL = "https://app.zenserp.com/api/v2/status"
SEARCH_URL = "https://app.zenserp.com/api/v2/search"


class Client:
    def __init__(self, api_key: str):
        """The client to request Zenserp.

        Args:
            api_key (str): Your API key of Zenserp.
        """
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

    def status(self) -> Status:
        """Checks the remaining requests of your API key.

        Returns:
            :class:`Status`: The status of your API key.
        """
        with self._session.get(STATUS_URL) as resp:
            resp.encoding = resp.apparent_encoding
            self.handle_error(resp)
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
            query (str): A keyword to query.
            location (:obj:`str`, optional): A geolocation used in the query.
            search_engine (:obj:`str`, optional): A URL of the search engine to query.
            limit (:obj:`int`, optional): A number of search results. It can be 1 - 100.
            offset (:obj:`int`, optional): An offset for the search results.
            tbm (:obj:`TBM`, optional): A type of the Google Search.
            device (:obj:`Device`, optional): A device to use for the Google Search.
            timeframe (:obj:`str`, optional): Time interval of you interests.
            gl (:obj:`str`, optional):
                A country code that means the country to use for the Google Search.
                It is automatically detected from the 'search_engine' if not supplied.
            lr (:obj:`str`, optional):
                One or multiple country codes that limits languages the Google Search.
                It is automatically detected from the 'search_engine' if not supplied.
            hl (:obj:`str`, optional):
                A language code that means the language to use for the Google Search.
                It is automatically detected from the 'search_engine' if not supplied.
            latitude (:obj:`str`, optional): A latitude of a geolocation used in the query.
            longitude (:obj:`str`, optional): A longitude of a geolocation used in the query.

        Returns:
            dict: Search results from the search via Zenserp.
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
        with self._session.get(SEARCH_URL, params=search_input.to_params()) as resp:
            resp.encoding = resp.apparent_encoding
            self.handle_error(resp)
            return cast(SERP, resp.json())
