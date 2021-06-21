import json
import sys
from dataclasses import asdict
from typing import Optional

import click

from .client import Client
from .search import TBM, Device

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option("-k", "--api-key", type=str, help="Your API key of Zenserp.", required=True)
@click.pass_context
def cli(ctx: click.Context, api_key: str) -> None:
    """The CLI to request Zenserp."""
    ctx.ensure_object(str)
    ctx.obj = api_key


@cli.command()
@click.pass_obj
def status(api_key: str) -> None:
    """Checks the status of your API key."""
    with Client(api_key) as c:
        try:
            status = c.status()
        except Exception as e:
            click.echo(message=e, err=True)
            sys.exit(1)
        else:
            click.echo(message=json.dumps(asdict(status), ensure_ascii=False, indent=2))


@cli.command()
@click.argument("query", type=str)
@click.option("--location", type=str, help="A geolocation used in the query.")
@click.option("--search-engine", type=str, help="A URL of the search engine to query.")
@click.option("--limit", type=click.IntRange(1, 100), help="A number of the search results.")
@click.option("--offset", type=int, help="An offset for the search results.")
@click.option("--tbm", type=click.Choice(["isch", "vid", "lcl", "nws", "shop"]), help="A type of the Google Search.")
@click.option("--device", type=click.Choice(["desktop", "mobile"]), help="A device used for the Google Search.")
@click.option("--timeframe", type=str, help="Time interval of your interest.")
@click.option("--gl", type=str, help="A country code that means the country to used for the Google Search.")
@click.option("--lr", type=str, help="One or multiple country codes that limits languages the Google Search.")
@click.option("--hl", type=str, help="A language code that means the language to use for the Google Search.")
@click.option("--latitude", type=str, help="A latitude of a geolocation used in the query.")
@click.option("--longitude", type=str, help="A longitude of a geolocation used in the query.")
@click.pass_obj
def search(
    api_key: str,
    query: str,
    location: Optional[str] = None,
    search_engine: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    tbm: Optional[str] = None,
    device: Optional[str] = None,
    timeframe: Optional[str] = None,
    gl: Optional[str] = None,
    lr: Optional[str] = None,
    hl: Optional[str] = None,
    latitude: Optional[str] = None,
    longitude: Optional[str] = None,
) -> None:
    """Google Search."""
    with Client(api_key) as c:
        try:
            serp = c.search(
                query,
                location=location,
                search_engine=search_engine,
                limit=limit,
                offset=offset,
                tbm=None if tbm is None else TBM(tbm),
                device=None if device is None else Device(device),
                timeframe=timeframe,
                gl=gl,
                lr=lr,
                hl=hl,
                latitude=latitude,
                longitude=longitude,
            )
        except Exception as e:
            click.echo(message=e, err=True)
            sys.exit(1)
        else:
            click.echo(message=json.dumps(serp, ensure_ascii=False, indent=2))


@cli.command()
@click.pass_obj
def hl(api_key: str) -> None:
    """List all supported hl parameters."""
    with Client(api_key) as c:
        try:
            hl = c.hl()
        except Exception as e:
            click.echo(message=e, err=True)
            sys.exit(1)
        else:
            click.echo(message=json.dumps(hl, ensure_ascii=False, indent=2))


@cli.command()
@click.pass_obj
def gl(api_key: str) -> None:
    """List all supported gl parameters."""
    with Client(api_key) as c:
        try:
            gl = c.gl()
        except Exception as e:
            click.echo(message=e, err=True)
            sys.exit(1)
        else:
            click.echo(message=json.dumps(gl, ensure_ascii=False, indent=2))


@cli.command()
@click.pass_obj
def locations(api_key: str) -> None:
    """List all supported geo locations."""
    with Client(api_key) as c:
        try:
            locations = c.locations()
        except Exception as e:
            click.echo(message=e, err=True)
            sys.exit(1)
        else:
            click.echo(message=json.dumps(locations, ensure_ascii=False, indent=2))


@cli.command()
@click.pass_obj
def search_engines(api_key: str) -> None:
    """List all supported Google search engines."""
    with Client(api_key) as c:
        try:
            search_engines = c.search_engines()
        except Exception as e:
            click.echo(message=e, err=True)
            sys.exit(1)
        else:
            click.echo(message=json.dumps(search_engines, ensure_ascii=False, indent=2))
