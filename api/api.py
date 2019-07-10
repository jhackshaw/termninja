import sanic_jwt
from sanic import Sanic
from sanic.response import json
from sanic.exceptions import InvalidUsage
from user import bp as user_bp, authenticate, retrieve_user
from game import bp as game_bp
from rounds import bp as round_bp
from termninja import db

app = Sanic()


@app.listener('after_server_start')
async def setup_db(app, loop):
    await db.conn.connect()

@app.listener('after_server_stop')
async def close_db(app, loop):
    await db.conn.disconnect()

@app.exception(InvalidUsage)
async def bad_request_handler(request, exception):
    return json({'message': str(exception)}, status=400)

app.blueprint(user_bp)
app.blueprint(game_bp)
app.blueprint(round_bp)

sanic_jwt.initialize(
    app, 
    authenticate=authenticate,
    retrieve_user=retrieve_user
)

