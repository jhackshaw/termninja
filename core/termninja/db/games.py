import datetime
from sqlalchemy import (select,
                        insert,
                        update)
from slugify import slugify
from .conn import conn
from .tables import games_table


async def create_or_update_game(slug, values):
    """
    Called once by server.PingDatabaseMixin on startup
    """
    query = select([games_table])\
                .where(games_table.c.slug == slug)
    result = await conn.fetch_one(query=query)
    if result is None:
        await create_game(slug, values)
    else:
        await update_game(slug, values)


async def create_game(slug, values):
    query = insert(games_table)
    create_values = {
        'slug': slug,
        'last_active': datetime.datetime.now(),
        **values
    }
    await conn.execute(query=query, values=create_values) 


async def update_game(slug, values={}):
    query = update(games_table)\
                .where(games_table.c.slug == slug)
    update_values = {
        'last_active': datetime.datetime.now(),
        **values
    }
    await conn.execute(query=query, values=update_values)


async def list_games():
    query = select([games_table])\
                .order_by('port')
    return [
        dict(r) for r in 
        await conn.fetch_all(query=query)
    ]


async def get_game(slug):
    query = select([games_table])\
                .where(games_table.c.slug == slug)
    res = await conn.fetch_one(query=query)
    return res and dict(res)
