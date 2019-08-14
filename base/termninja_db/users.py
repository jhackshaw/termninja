import datetime
import hashlib
import os
from uuid import uuid4
from passlib.hash import pbkdf2_sha256
from sqlalchemy import (insert,
                        select,
                        update)
from .conn import conn
from .tables import users_table


GLOBAL_LEADERBOARD_SIZE = os.environ.get(
    'TERMNINJA_GLOBAL_LEADERBOARD_SIZE', 25
)

default_columns = [
    users_table.c.id,
    users_table.c.username,
    users_table.c.gravatar_hash,
    users_table.c.total_score
]

authenticated_columns = [
    *default_columns,
    users_table.c.play_token,
    users_table.c.play_token_expires_at
]


def make_token():
    return str(uuid4())


def make_token_expires_at(days):
    now = datetime.datetime.now()
    return now + datetime.timedelta(days=days)


def create_gravatar_hash(username):
    return hashlib.md5(username.encode()).hexdigest()


def create_password_hash(password):
    return pbkdf2_sha256.hash(password)


def verify_password(password, password_hash):
    return pbkdf2_sha256.verify(password, password_hash)


async def create_user(username, password):
    """
    Create a user, returns new user_id
    """
    values = {
        'username': username,
        'password_hash': create_password_hash(password),
        'gravatar_hash': create_gravatar_hash(username),
        'play_token': make_token(),
        'play_token_expires_at': make_token_expires_at(1)
    }
    query = insert(users_table)
    return await conn.execute(query=query, values=values)


async def verify_login(username, password):
    """
    Return user if username and password are valid
    """
    # this needs to select all columns, we need the password
    query = select([users_table])\
              .where(users_table.c.username == username)  # noqa:E127
    user = await conn.fetch_one(query=query)
    if user and verify_password(password, user['password_hash']):
        return dict(user)
    return None


async def select_by_username(username, authenticated=False):
    """
    Get a user by username
    """
    columns = authenticated_columns if authenticated else default_columns
    query = select(columns)\
              .where(users_table.c.username == username)  # noqa:E127
    user = await conn.fetch_one(query=query)
    return user and dict(user)


async def select_by_play_token(token):
    """
    Get a user by their play token
    """
    query = select(authenticated_columns)\
                .where(users_table.c.play_token == token)  # noqa:E127
    user = await conn.fetch_one(query=query)
    return user and dict(user)


async def refresh_play_token(username, days=7):
    """
    Give a user a new play token with more time
        username is expected to exist.
    """
    query = update(users_table)\
                .where(users_table.c.username == username)  # noqa:E127
    values = {
        'play_token': make_token(),
        'play_token_expires_at': make_token_expires_at(days=days)
    }
    await conn.execute(query=query, values=values)
    return await select_by_username(username, authenticated=True)


async def increment_score(username, earned):
    """
    Give more points to a user
    """
    query = update(users_table)\
                .where(users_table.c.username == username)\
                .values(users_table.c.score + earned)  # noqa:E127
    await conn.execute(query=query)


async def list_global_leaderboard():
    """
    Users with the highest combined score of all games
    """
    query = select([users_table])\
                .limit(GLOBAL_LEADERBOARD_SIZE)\
                .order_by(users_table.c.total_score.desc())  # noqa:E127
    leaders = await conn.fetch_all(query=query)
    return leaders and [
        dict(l) for l in leaders
    ]
