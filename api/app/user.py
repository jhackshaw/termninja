import termninja_db as db
from sanic import Blueprint
from sanic.response import json, text
from sanic.exceptions import abort
from asyncpg.exceptions import UniqueViolationError
from .validators import validate_page
from .decorators import cache, throttle


bp = Blueprint('user_views', url_prefix="/user")


async def get_user_from_creds(username, password):
    if not (username and password):
        abort(400)
    user = await db.users.verify_login(username, password)
    if user is None:
        abort(400)
    return user


@bp.route('/', methods=['POST'])
@throttle(max_per_minute=1, prefix='create_user')
async def create_user(request):
    """
    Create a user
    """
    username = request.form.get('username')
    password = request.form.get('password')
    if not (username and password):
        abort(400, 'username and password required')
    try:
        user_id = await db.users.create_user(username, password)
    except UniqueViolationError:
        abort(400, 'username is taken')
    return json({'user_id': user_id}, status=201)


@bp.route('/', methods=['GET'])
@cache()
async def list_leaderboard(request):
    """
    List top users by score
    """
    leaders = await db.users.list_global_leaderboard()
    return json(leaders)


@bp.route('/<username>', methods=['GET'])
async def get_user_details(request, username):
    """
    Depending on whether or not the user is authenticated
    as <username> return all user columns
    """
    user = await db.users.select_by_username(username)
    if not user:
        abort(404)
    return json(user)


@bp.route('/<username>/rounds', methods=['GET'])
@cache()
async def list_rounds_by_user(request, username):
    request_page = request.args.get('page', '0')
    page = validate_page(request_page)
    results = await db.rounds.list_rounds_played(page=page,
                                                 user_username=username)
    return json(results)


@bp.route('/retrieve_play_token', methods=['POST'])
@throttle(max_per_minute=2, prefix='retrieve_play_token')
async def retrieve_play_token(request):
    """
    Get a play token for a user. Used by client script to login.
    """
    username = request.form.get('username')
    password = request.form.get('password')
    user = await get_user_from_creds(username, password)
    return text(user['play_token'])
