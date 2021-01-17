import logging

from lark.exceptions import UnexpectedInput
from quart import abort
from quart import jsonify
from quart import Response
from quart_trio import QuartTrio

from toy_address_parser.parser import parse

app = QuartTrio(__name__)
logger = logging.getLogger(__name__)


@app.route('/_internal/health')
async def check_alive():
    return 'Hello world!'


@app.route('/parse/<address>')
async def parse_address(address: str):
    logger.debug('Input: ``%s``', address)
    try:
        return jsonify(parse(address))

    except UnexpectedInput as exc:
        logger.info('Failed parse: ``%s``', address, exc_info=exc)
        abort(Response('Error: does not appear to be an address.', 400))
