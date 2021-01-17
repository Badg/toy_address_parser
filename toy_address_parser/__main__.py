import json
import logging
from typing import Optional

import trio
import typer
from hypercorn.config import Config
from hypercorn.trio import serve as hypercorn_serve

from toy_address_parser.app import app as parser_webapp
from toy_address_parser.app import logger as webapp_logger
from toy_address_parser.parser import parse as parse_address


DEFAULT_USE_PORT = 8000
cli_app = typer.Typer()


@cli_app.command()
def serve(
    port: Optional[str] = typer.Argument(None),
    debug: Optional[bool] = typer.Option(False, '--debug')
):
    if port is None:
        port = DEFAULT_USE_PORT

    if debug:
        webapp_logger.setLevel(logging.DEBUG)

    log_handler = logging.StreamHandler()
    log_formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(name)s: %(message)s')
    log_handler.setFormatter(log_formatter)
    webapp_logger.addHandler(log_handler)
    trio.run(webapp_main, port)


@cli_app.command()
def parse(address: str):
    typer.echo(f'Input: ``{address}``\n-----\n')
    typer.echo(json.dumps(parse_address(address)))


async def webapp_main(port):
    config = Config()
    config.bind = [f'localhost:{port}']

    await hypercorn_serve(parser_webapp, config)


if __name__ == '__main__':
    cli_app()
