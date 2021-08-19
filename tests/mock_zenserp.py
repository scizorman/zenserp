import json
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Coroutine

from aiohttp import web

VALID_API_KEY = "VALID_API_KEY"
TEST_DATA_DIR = Path(__file__).parent / "data"

MockZenserpAPIFunction = Callable[[web.Request], Coroutine[Any, Any, web.Response]]


def validate_api_key(func: MockZenserpAPIFunction) -> MockZenserpAPIFunction:
    @wraps(func)
    async def wrapper(request: web.Request) -> web.Response:
        api_key = request.headers.get("apikey")
        if api_key == VALID_API_KEY:
            return await func(request)
        elif api_key == "" or api_key is None:
            data = {"error": "No apikey provided."}
            return web.json_response(data, status=403)
        else:
            data = {"error": "Not enough requests."}
            return web.json_response(data, status=403)

    return wrapper


routes = web.RouteTableDef()


@routes.get("/status")
@validate_api_key
async def status(_: web.Request) -> web.Response:
    with (TEST_DATA_DIR / "status.json").open() as f:
        data = json.load(f)
    return web.json_response(data)


@routes.get("/hl")
@validate_api_key
async def hl(_: web.Request) -> web.Response:
    with (TEST_DATA_DIR / "hl.json").open() as f:
        data = json.load(f)
    return web.json_response(data)


@routes.get("/gl")
@validate_api_key
async def gl(_: web.Request) -> web.Response:
    with (TEST_DATA_DIR / "gl.json").open() as f:
        data = json.load(f)
    return web.json_response(data)


@routes.get("/locations")
@validate_api_key
async def locations(_: web.Request) -> web.Response:
    with (TEST_DATA_DIR / "locations.json").open() as f:
        data = json.load(f)
    return web.json_response(data)


@routes.get("/search_engines")
@validate_api_key
async def search_engines(_: web.Request) -> web.Response:
    with (TEST_DATA_DIR / "search_engines.json").open() as f:
        data = json.load(f)
    return web.json_response(data)


def init_mock_zenserp() -> web.Application:
    app = web.Application()
    app.add_routes(routes)
    return app
