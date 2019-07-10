import datetime
from sqlalchemy import (insert,
                        select)
from .conn import conn
from .tables import rounds_table


PAGE_SIZE = 20

list_columns = [
    rounds_table.c.id,
    rounds_table.c.played_at,
    rounds_table.c.game_friendlyname,
    rounds_table.c.user_username,
    rounds_table.c.score,
    rounds_table.c.result_message
]

detail_columns = list_columns + [
    rounds_table.c.result_snapshot
]


async def add_round_played(friendly_name, username, score, 
                           result_message='', result_snapshot=''):
    query = insert(rounds_table)
    values = {
        'game_friendlyname': friendly_name,
        'user_username': username,
        'score': score,
        'played_at': datetime.datetime.now(),
        'result_message': result_message,
        'result_snapshot': result_snapshot
    }
    await conn.execute(query=query, values=values)


async def list_rounds_played(page=0):
    query = select(list_columns)\
                .order_by(rounds_table.c.played_at.desc())\
                .limit(PAGE_SIZE)\
                .offset(page * PAGE_SIZE)
    result = await conn.fetch_all(query=query)
    return result and [
        dict(r) for r in result
    ]


async def get_round_details(round_id):
    query = select(detail_columns)\
                .where(rounds_table.c.id == round_id)
    result = await conn.fetch_one(query=query)
    return result and dict(result)
