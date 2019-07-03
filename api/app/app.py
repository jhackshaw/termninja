from sanic import Sanic
from sanic.response import json
from sanic.exceptions import InvalidUsage
import sanic_jwt
from user import bp as user_bp, authenticate
from termninja.db import db, users

app = Sanic()

@app.listener('after_server_start')
async def setup_db(app, loop):
    app.db = db
    await app.db.connect()

@app.listener('after_server_stop')
async def close_db(app, loop):
    await app.db.disconnect()

@app.exception(InvalidUsage)
async def bad_request_handler(request, exception):
    return json({'message': str(exception)}, status=400)

app.blueprint(user_bp)

sanic_jwt.initialize(app, authenticate=authenticate)