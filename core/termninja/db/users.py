import datetime
from sqlalchemy import insert, Column, String, Integer, Table, DateTime
from uuid import uuid4
from passlib.hash import pbkdf2_sha256
from .exceptions import NotFoundError
from .db import metadata, db

def make_token():
    return str(uuid4())

def make_token_expires_at():
    now = datetime.datetime.now()
    return now + datetime.timedelta(days=1)

table = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(64), nullable=False, unique=True),
    Column('password_hash', String(128), nullable=False),
    Column('play_token', String(36), nullable=False),
    Column('play_token_expires_at', DateTime(), nullable=False)
)

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
        'play_token_expires_at': make_token_expires_at()
    }
    query = table.insert(None)
    return await db.execute(query=query, values=values)

async def verify_login(username, password):
    """
    Return userid if username and password are valid
    """
    user = table.select()\
                .where(table.c.username == username)
    if verify_password(password, user['password_hash']):
        return user
    return None

async def get_user(user_id):
    """
    Get a user by id
    """
    query = table.select()\
                 .where(table.c.id == user_id)
    return await db.fetch_one(query=query)


