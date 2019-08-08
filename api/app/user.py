import termninja_db as db
from sanic import Blueprint
from sanic.response import json
from sanic.exceptions import abort
from sanic_jwt import BaseEndpoint
from sanic_jwt.exceptions import AuthenticationFailed
from sanic_jwt.decorators import protected, inject_user
from asyncpg.exceptions import UniqueViolationError
from .validators import validate_page


bp = Blueprint('user_views', url_prefix="/user")


class LogoutEndpoint(BaseEndpoint):
    async def get(self, request, *args, **kwargs):
        """
        Delete authentication cookie to effectively log user out
        """
        response = json({})
        config = request.app.config
        domain = config['SANIC_JWT_COOKIE_DOMAIN']
        token_name = config['SANIC_JWT_COOKIE_ACCESS_TOKEN_NAME']
        http_only = config['SANIC_JWT_COOKIE_HTTPONLY']

        response.cookies[token_name] = 'deleted'
        response.cookies[token_name]['max-age'] = 0
        response.cookies[token_name]['domain'] = domain
        response.cookies[token_name]['httponly'] = http_only

        return response


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
            payload.get('username', None),
            authenticated=True
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
async def list_leaderboard(request):
    """
    List top users by score
    """
    leaders = await db.users.list_global_leaderboard()
    return json(leaders)


@bp.route('/<username>', methods=['GET'])
@inject_user()
async def get_user_details(request, username, user):
    """
    Depending on whether or not the user is authenticated
    as <username> return all user columns
    """
    authenticated = user and user.get('username') == username
    user = await db.users.select_by_username(username,
                                             authenticated=authenticated)
    if not user:
        abort(404)
    return json(user)


@bp.route('/<username>/rounds', methods=['GET'])
async def list_rounds_by_user(request, username):
    request_page = request.args.get('page', '0')
    page = validate_page(request_page)
    results = await db.rounds.list_rounds_played(page=page,
                                                 user_username=username)
    return json(results)


@bp.route('/refresh_play_token', methods=['POST'])
@inject_user()
@protected()
async def refresh_token(request, user):
    res = await db.users.refresh_play_token(user['username'])
    return json({
        'play_token': res['play_token'],
        'play_token_expires_at': res['play_token_expires_at']
    })
