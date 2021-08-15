import json
from pathlib import Path

from aiohttp import web

VALID_API_KEY = "VALID_API_KEY"
TEST_DATA_DIR = Path(__file__).parent / "data"

routes = web.RouteTableDef()


@routes.get("/status")
async def status(_: web.Request) -> web.Response:
    with (TEST_DATA_DIR / "status.json").open() as f:
        data = json.load(f)
    return web.json_response(data)


@routes.get("/hl")
async def hl(_: web.Request) -> web.Response:
    with (TEST_DATA_DIR / "hl.json").open() as f:
        data = json.load(f)
    return web.json_response(data)


@routes.get("/gl")
async def gl(_: web.Request) -> web.Response:
    with (TEST_DATA_DIR / "gl.json").open() as f:
        data = json.load(f)
    return web.json_response(data)


@routes.get("/locations")
async def locations(_: web.Request) -> web.Response:
    with (TEST_DATA_DIR / "locations.json").open() as f:
        data = json.load(f)
    return web.json_response(data)


@routes.get("/search_engines")
async def search_engines(_: web.Request) -> web.Response:
    with (TEST_DATA_DIR / "search_engines.json").open() as f:
        data = json.load(f)
    return web.json_response(data)


def init_mock_zenserp() -> web.Application:
    app = web.Application()
    app.add_routes(routes)
    return app
