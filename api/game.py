from sanic import Blueprint
from sanic.response import json
from termninja import db


bp = Blueprint('game_views', url_prefix='/game')


@bp.route('/', methods=['GET'])
async def list_games(request):
    all_games = await db.games.list_games()
    return json(all_games)
