from sanic import Blueprint
from sanic.response import json
from sanic.exceptions import abort
from termninja import db


bp = Blueprint('game_views', url_prefix='/game')


@bp.route('/', methods=['GET', 'OPTIONS'])
async def list_games(request):
    all_games = await db.games.list_games()
    return json(all_games)


@bp.route('/<slug>')
async def get_game(request, slug):
    game = await db.games.get_game(slug)
    if game is None:
        abort(404)
    return json(game)
