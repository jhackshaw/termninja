import termninja_db as db
from sanic import Blueprint
from sanic.response import json
from sanic.exceptions import abort
from .validators import validate_page
from .decorators import cache


bp = Blueprint('round_views', url_prefix='/round')


@bp.route('/', methods=['GET'])
async def list_rounds(request):
    request_page = request.args.get('page', '0')
    page = validate_page(request_page)
    results = await db.rounds.list_rounds_played(page=page)
    return json(results)


@bp.route('/<round_id:int>', methods=['GET'])
@cache(seconds_until_expire=60*10, max_age=60*60*24)
async def get_round_details(request, round_id):
    result = await db.rounds.get_round_details(round_id)
    if result is None:
        abort(404)
    return json(result)
