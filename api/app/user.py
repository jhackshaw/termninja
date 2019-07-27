import termninja_db as db
from sanic import Blueprint
from sanic.response import json
from sanic.exceptions import abort
from sanic_jwt.exceptions import AuthenticationFailed
from sanic_jwt.decorators import protected, inject_user
from asyncpg.exceptions import UniqueViolationError


bp = Blueprint('user_views', url_prefix="/user")


async def authenticate(request):
    """
    Used by sanic-jwt for the auth/login endpoint.
    """
    username = request.json.get('username')
    password = request.json.get('password')
    if not (username and password):
        abort(400)
    user = await db.users.verify_login(username, password)
    if user is None:
        raise AuthenticationFailed
    return dict(user)


async def retrieve_user(request, payload):
    """
    Used by sanic-jwt to retrieve a user from a token
    """
    if payload:
        user = await db.users.select_by_username(
            payload.get('username', None)
        )
        return user and dict(user)
    return None


async def extend_jwt_payload(payload, user):
    """
    Add additional user information to the jwt
    """
    score = user['score']
    payload.update({
        'score': score,
    })
    return payload


@bp.route('/', methods=['POST'])
async def create_user(request):
    """
    Create a user
    """
    username = request.json.get('username')
    password = request.json.get('password')
    if not (username and password):
        abort(400, 'username and password required')
    try:
        user_id = await db.users.create_user(username, password)
    except UniqueViolationError:
        abort(400, 'username is taken')
    return json({'user_id': user_id})


@bp.route('/', methods=['GET'])
async def list_users(request):
    """
    List users
    """
    return json({'users': 'come back later'})


@bp.route('/refresh_play_token', methods=['POST'])
@inject_user()
@protected()
async def refresh_token(request, user):
    days = request.json.get('days', 5)
    if not isinstance(days, int) or not 0 < days <= 5:
        abort(400, "invalid delta")
    res = await db.users.refresh_play_token(user['username'], days=days)
    return json({
        'play_token': res['play_token'],
        'play_token_expires_at': res['play_token_expires_at']
    })
