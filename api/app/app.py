from sanic import Sanic, response
from termninja.db import db

app = Sanic()

@app.listener('after_server_start')
async def setup_db(app, loop):
    app.db = db
    await app.db.connect()


@app.listener('after_server_stop')
async def close_db(app, loop):
    await app.db.disconnect()


@app.route('/')
async def ping(request):
    query = "SELECT * FROM alembic_version;"
    res = await db.fetch_all(query=query)
    print(res[0], dict(res[0]))
    return response.json(res)