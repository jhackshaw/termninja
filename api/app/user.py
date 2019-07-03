from sanic import Blueprint
from sanic.views import HTTPMethodView
from sanic.response import json
from sanic.exceptions import abort
from sanic_jwt.exceptions import AuthenticationFailed
from asyncpg.exceptions import UniqueViolationError
from termninja.db import users


bp = Blueprint('user_views', url_prefix="/user")


async def authenticate(request):
    username = request.json.get('username')
    password = request.json.get('password')
    if not (username and password):
        abort(400)
    user = await users.verify_login(username, password)
    if user is None:
        raise AuthenticationFailed
    return user


class UserListView(HTTPMethodView):
    async def post(self, request):
        """
        Endpoint to create a user
        """
        username = request.json.get('username')
        password = request.json.get('password')
        if not (username and password):
            abort(400, 'username and password required')
        try:
            user_id = await users.create_user(username, password)
            return json({'user_id': user_id})
        except UniqueViolationError:
            abort(400, 'username is already taken')

bp.add_route(UserListView.as_view(), '/')
