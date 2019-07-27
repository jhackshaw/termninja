import termninja_db as db
import sanic_jwt
from sanic import Sanic
from sanic.response import json, text
from sanic.exceptions import InvalidUsage
from .user import bp as user_bp, authenticate, retrieve_user
from .game import bp as game_bp
from .rounds import bp as round_bp


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


@app.exception(sanic_jwt.exceptions.AuthenticationFailed)
async def bad_login_handler(request, exception):
    return json({'message': 'Login Failed'}, status=401)


app.blueprint(user_bp)
app.blueprint(game_bp)
app.blueprint(round_bp)


@app.middleware('request')
def options(request):
    if request.method == "OPTIONS":
        print('returning options')
        return text('')


@app.middleware('response')
def add_cors_headers(request, response):
    response.headers.update({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': '*'
    })


sanic_jwt.initialize(
    app,
    authenticate=authenticate,
    retrieve_user=retrieve_user
)
