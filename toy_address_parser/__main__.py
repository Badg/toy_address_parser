import trio
from hypercorn.config import Config
from hypercorn.trio import serve

from toy_address_parser.app import app

DEFAULT_USE_PORT = 8000


async def main(use_port=None):
    if use_port is None:
        use_port = DEFAULT_USE_PORT

    config = Config()
    config.bind = [f'localhost:{use_port}']

    await serve(app, config)


if __name__ == '__main__':
    trio.run(main)
