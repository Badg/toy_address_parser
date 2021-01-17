from quart_trio import QuartTrio

app = QuartTrio(__name__)


@app.route('/_internal/health')
async def check_alive():
    return 'Hello world!'
