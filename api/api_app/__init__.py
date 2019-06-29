from api_app.settings import DATABASE_URL
from sanic import Sanic, response
from databases import Database


app = Sanic()


@app.listener('after_server_start')
async def setup_db(app, loop):
    app.db = Database(DATABASE_URL)
    await app.db.connect()


@app.listener('after_server_stop')
async def close_db(app, loop):
    await app.db.disconnect()


@app.route('/')
async def ping(request):
    return response.text('pong')


def start_app():
    app.run('0.0.0.0', 3000)
