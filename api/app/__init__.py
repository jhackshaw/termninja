import termninja_db as db
import sanic_jwt
import os
from sanic import Sanic
from sanic.response import json, text
from sanic.exceptions import InvalidUsage
from .user import (bp as user_bp,
                   authenticate,
                   retrieve_user,
                   extend_jwt_payload,
                   LogoutEndpoint)
from .game import bp as game_bp
from .rounds import bp as round_bp


app = Sanic()

frontend_host = os.environ.get('TERMNINJA_FRONTEND_HOST',
                               'http://localhost:3000')


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
        return text('')


@app.middleware('response')
def add_cors_headers(request, response):
    response.headers.update({
        'Access-Control-Allow-Origin': frontend_host,
        'Access-Control-Allow-Headers': 'Content-Type,Authorization',
        'Access-Control-Allow-Credentials': 'true'
    })


sanic_jwt.initialize(
    app,
    authenticate=authenticate,
    retrieve_user=retrieve_user,
    extend_payload=extend_jwt_payload,
    class_views=(
        ('/logout', LogoutEndpoint),
    )
)
