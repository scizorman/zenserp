import sys

import click

from .client import Client

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option(
    "-k",
    "--api-key",
    type=str,
    help="Your API key of Zenserp",
    required=True,
)
@click.pass_context
def cli(ctx: click.Context, api_key: str):
    """The CLI to request Zenserp."""
    ctx.obj = api_key


@cli.command()
@click.pass_obj
def status(api_key: str):
    """Checks the remaining request of your API key."""
    with Client(api_key) as c:
        try:
            remaining_requests = c.status()
        except Exception as e:
            click.echo(message=e, err=True)
            sys.exit(1)
        else:
            click.echo(message=remaining_requests)
