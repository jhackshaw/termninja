import datetime
from uuid import uuid4
from passlib.hash import pbkdf2_sha256
from sqlalchemy import (insert,
                        select,
                        update)
from .conn import conn
from .tables import users_table


default_columns = [
    users_table.c.id,
    users_table.c.username,
    users_table.c.play_token,
    users_table.c.play_token_expires_at,
    users_table.c.score
]


def make_token():
    return str(uuid4())


def make_token_expires_at(days):
    now = datetime.datetime.now()
    return now + datetime.timedelta(days=days)


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


async def select_by_username(username):
    """
    Get a user by username
    """
    query = select(default_columns)\
              .where(users_table.c.username == username)  # noqa:E127
    user = await conn.fetch_one(query=query)
    return user and dict(user)


async def select_by_play_token(token):
    """
    Get a user by their play token
    """
    query = select(default_columns)\
                .where(users_table.c.play_token == token)  # noqa:E127
    user = await conn.fetch_one(query=query)
    return user and dict(user)


async def refresh_play_token(username, days=1):
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
    return await select_by_username(username)


async def increment_score(username, earned):
    """
    Give more points to a user
    """
    query = update(users_table)\
                .where(users_table.c.username == username)\
                .values(users_table.c.score + earned)  # noqa:E127
    await conn.execute(query=query)
