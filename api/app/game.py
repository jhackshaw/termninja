import termninja_db as db
from sanic import Blueprint
from sanic.response import json
from sanic.exceptions import abort
from .validators import validate_page
from .decorators import cache


bp = Blueprint('game_views', url_prefix='/game')


@bp.route('/')
@cache('games-list')
async def list_games(request):
    all_games = await db.games.list_games()
    print(all_games)
    return json(all_games)


@bp.route('/<slug>')
@cache()
async def get_game(request, slug):
    game = await db.games.get_game(slug)
    if game is None:
        abort(404)
    return json(game)


@bp.route('/<slug>/round')
@cache()
async def list_rounds_for_game(request, slug):
    request_page = request.args.get('page', '0')
    page = validate_page(request_page)
    results = await db.rounds.list_rounds_played(page=page, game_slug=slug)
    return json(results)


@bp.route('/<slug>/leaderboard')
@cache()
async def leaderboard(request, slug):
    results = await db.rounds.list_high_scores(game_slug=slug)
    return json(results)
