import datetime
from sqlalchemy import (select,
                        insert,
                        update)
from .conn import conn
from .tables import games_table


async def register_server(friendly_name, port):
    """
    Called once by server.PingDatabaseMixin on startup
    """
    query = select([games_table])\
                .where(games_table.c.friendlyname == friendly_name)
    result = await conn.fetch_one(query=query)
    if result is None:
        await create_game(friendly_name, port)


async def create_game(friendly_name, port):
    query = insert(games_table)
    values = {
        'friendlyname': friendly_name,
        'port': port,
        'last_active': datetime.datetime.now()
    }
    await conn.execute(query=query, values=values) 


async def ping(friendly_name, port):
    query = update(games_table)
    values = {
        'port': port,
        'last_active': datetime.datetime.now()
    }
    await conn.execute(query=query, values=values)


async def list_games():
    query = select([games_table])
    return [
        dict(r) for r in 
        await conn.fetch_all(query=query)
    ]
