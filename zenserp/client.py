from __future__ import annotations

from types import TracebackType
from typing import Iterable, Optional, Type, cast

from aiohttp import ClientSession

from .model import GL, HL, SERP, TBM, Device, Location, SearchEngine, Status


class Client:

    base_url = "https://app.zenserp.com/api/v2"

    def __init__(self, api_key: str) -> None:
        """The asynchronous client to request Zenserp.

        Args:
            api_key (str): Your API key of Zenserp.
        """
        headers = {"apikey": api_key}
        self.__session = ClientSession(headers=headers)

    async def __aenter__(self) -> Client:
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self.close()

    async def close(self) -> None:
        """Closes this client."""
        await self.__session.close()

    async def status(self) -> Status:
        """Checks the status of your API key.

        Returns:
            The status of your API key.
        """
        url = f"{self.base_url}/status"
        async with self.__session.get(url) as resp:
            body = await resp.json()
            return Status(body["remaining_requests"])

    async def search(
        self,
        query: str,
        location: Optional[Location] = None,
        search_engine: Optional[SearchEngine] = None,
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
        url = f"{self.base_url}/search"
        params = {
            k: v
            for k, v in {
                "q": query,
                "location": location,
                "search_engine": search_engine,
                "num": limit,
                "start": offset,
                "tbm": None if tbm is None else tbm.value,
                "device": None if device is None else device.value,
                "timeframe": timeframe,
                "gl": gl,
                "lr": lr,
                "hl": hl,
                "lat": latitude,
                "lng": longitude,
            }.items()
            if v is not None
        }
        async with self.__session.get(url, params=params) as resp:
            body = await resp.json()
            return cast(SERP, body)

    async def hl(self) -> Iterable[HL]:
        """List all supported hl parameters.

        Returns:
            All supported hl parameters.
        """
        url = f"{self.base_url}/hl"
        async with self.__session.get(url) as resp:
            body = await resp.json()
            return [HL(row["code"], row["name"]) for row in body]

    async def gl(self) -> Iterable[GL]:
        """List all supported gl parameters.

        Returns:
            All supported gl parameters.
        """
        url = f"{self.base_url}/gl"
        async with self.__session.get(url) as resp:
            body = await resp.json()
            return [GL(row["code"], row["name"]) for row in body]

    async def locations(self) -> Iterable[Location]:
        """List all supported geo locations.

        Returns:
            All supported geo locations.
        """
        url = f"{self.base_url}/locations"
        async with self.__session.get(url) as resp:
            body = await resp.json()
            return [cast(Location, row) for row in body]

    async def search_engines(self) -> Iterable[SearchEngine]:
        """List all supported Google search engines.

        Returns:
            All supported Google search engines.
        """
        url = f"{self.base_url}/search_engines"
        async with self.__session.get(url) as resp:
            body = await resp.json()
            return [cast(SearchEngine, row) for row in body]
