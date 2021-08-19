from typing import Iterable

import pytest
from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop

from zenserp import Client
from zenserp.exceptions import APILimitException, NoAPIKeyException
from zenserp.model import GL, HL, Location, SearchEngine, Status

from .mock_zenserp import VALID_API_KEY, init_mock_zenserp


class TestClient(AioHTTPTestCase):
    async def get_application(self) -> web.Application:
        return init_mock_zenserp()

    @unittest_run_loop
    async def test_no_api_key_exception(self) -> None:
        with pytest.raises(NoAPIKeyException):
            async with Client("") as client:
                client.base_url = f"{self.server.scheme}://{self.server.host}:{self.server.port}"
                await client.status()

    @unittest_run_loop
    async def test_api_limit_exception(self) -> None:
        with pytest.raises(APILimitException):
            async with Client("LIMIT_EXHAUSTED_API_KEY") as client:
                client.base_url = f"{self.server.scheme}://{self.server.host}:{self.server.port}"
                await client.status()

    @unittest_run_loop
    async def test_status(self) -> None:
        async with Client(VALID_API_KEY) as client:
            client.base_url = f"{self.server.scheme}://{self.server.host}:{self.server.port}"
            status = await client.status()
        assert isinstance(status, Status)

    @unittest_run_loop
    async def test_hl(self) -> None:
        async with Client(VALID_API_KEY) as client:
            client.base_url = f"{self.server.scheme}://{self.server.host}:{self.server.port}"
            hls = await client.hl()
        assert isinstance(hls, Iterable)
        assert all(isinstance(hl, HL) for hl in hls)

    @unittest_run_loop
    async def test_gl(self) -> None:
        async with Client(VALID_API_KEY) as client:
            client.base_url = f"{self.server.scheme}://{self.server.host}:{self.server.port}"
            gls = await client.gl()
        assert isinstance(gls, Iterable)
        assert all(isinstance(gl, GL) for gl in gls)

    @unittest_run_loop
    async def test_locations(self) -> None:
        async with Client(VALID_API_KEY) as client:
            client.base_url = f"{self.server.scheme}://{self.server.host}:{self.server.port}"
            locations = await client.locations()
        assert isinstance(locations, Iterable)
        assert all(isinstance(location, Location) for location in locations)

    @unittest_run_loop
    async def test_search_engines(self) -> None:
        async with Client(VALID_API_KEY) as client:
            client.base_url = f"{self.server.scheme}://{self.server.host}:{self.server.port}"
            search_engines = await client.search_engines()
        assert isinstance(search_engines, Iterable)
        assert all(isinstance(search_engine, SearchEngine) for search_engine in search_engines)
