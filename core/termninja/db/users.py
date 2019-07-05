import datetime
from sqlalchemy import insert, Column, String, Integer, Table, DateTime
from uuid import uuid4
from .db import metadata, db

def make_token():
    return str(uuid4())

def make_token_expires_at():
    now = datetime.datetime.now()
    return now + datetime.timedelta(days=1)

users_table = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(64), nullable=False, unique=True),
    Column('token', String(36), nullable=False),
    Column('token_expires_at', DateTime(), nullable=False)
)

async def create_user(username):
    values = {
        'username': username,
        'token': make_token(),
        'token_expires_at': make_token_expires_at()
    }
    query = users_table.insert(None)
    return await db.execute(query=query, values=values)

async def get_user(username):
    query = users_table.select()\
                       .where(users_table.c.username == username)
    return await db.fetch_one(query=query)

async def get_user_from_token(token):
    query = users_table.select()\
                       .where(users_table.c.token == token)
    return await db.fetch_one(query=query)

async def reset_user_token(userid):
    query = users_table.update(None)\
                       .where(users_table.c.id == userid)
    values = {
        'token': make_token(),
        'token_expires_at': make_token_expires_at()
    }
    return await db.execute(query=query, values=values)
