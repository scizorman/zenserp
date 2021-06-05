import json
import sys
from typing import Optional

import click

from .client import Client

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option("-k", "--api-key", type=str, help="Your API key of Zenserp.", required=True)
@click.pass_context
def cli(ctx: click.Context, api_key: str) -> None:
    """The CLI to request Zenserp."""
    ctx.obj = api_key


@cli.command()
@click.pass_obj
def status(api_key: str) -> None:
    """Checks the remaining request of your API key."""
    with Client(api_key) as c:
        try:
            remaining_requests = c.status()
        except Exception as e:
            click.echo(message=e, err=True)
            sys.exit(1)
        else:
            click.echo(message=remaining_requests)


@cli.command()
@click.argument("query", type=str)
@click.option("--location", type=str, help="Geolocation used in the query.")
@click.option("--search-engine", type=str, help="URL of the search engine to query.")
@click.option("--limit", type=click.IntRange(1, 100), help="Number of search results.")
@click.option("--offset", type=int, help="Offset for the search results.")
@click.option("--tbm", type=click.Choice(["isch", "vid", "lcl", "nws", "shop"]), help="Type of search.")
@click.option("--device", type=click.Choice(["desktop", "mobile"]), help="Device to use.")
@click.option("--timeframe", type=str, help="Time interval of your interest.")
@click.option("--gl", type=str, help="A country code.")
@click.option("--lr", type=str, help="A country code.")
@click.option("--hl", type=str, help="Web interface language.")
@click.option("--latitude", type=str, help="Latitude of a geolocation used in the query.")
@click.option("--longitude", type=str, help="Longitude of a geolocation used in the query.")
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
                tbm=tbm,
                device=device,
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
