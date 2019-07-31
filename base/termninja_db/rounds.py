import datetime
from sqlalchemy import (insert,
                        select)
from .conn import conn
from .tables import rounds_table, games_table


PAGE_SIZE = 8

list_columns = [
    rounds_table.c.id,
    rounds_table.c.played_at,
    rounds_table.c.user_username,
    rounds_table.c.score,
    rounds_table.c.result_message,
    games_table.c.server_name,
    games_table.c.slug
]

detail_columns = list_columns + [
    rounds_table.c.result_snapshot
]


async def add_round_played(friendly_name, username, score,
                           result_message='', result_snapshot=''):
    query = insert(rounds_table)
    values = {
        'game_slug': friendly_name,
        'user_username': username,
        'score': score,
        'played_at': datetime.datetime.now(),
        'result_message': result_message,
        'result_snapshot': result_snapshot
    }
    await conn.execute(query=query, values=values)


async def list_rounds_played(page=0, **filters):
    where_clause = [
        getattr(rounds_table.c, k) == v
        for k, v in filters.items()
    ]
    # join user?
    query = select(list_columns)\
                .select_from(
                    rounds_table.join(
                        games_table,
                        rounds_table.c.game_slug == games_table.c.slug
                    ),
                )\
                .where(*where_clause)\
                .order_by(rounds_table.c.played_at.desc())\
                .limit(PAGE_SIZE)\
                .offset(page * PAGE_SIZE)  # noqa: E127
    result = await conn.fetch_all(query=query)
    rounds = result and [
        dict(r) for r in result
    ]

    next_page = None
    if len(result) == PAGE_SIZE:
        next_page = page+1
    
    prev_page = None
    if page > 0:
        prev_page = page-1
    
    return {
        'rounds': rounds,
        'next_page': next_page,
        'prev_page': prev_page
    }


async def get_round_details(round_id):
    query = select(detail_columns)\
                .select_from(
                    rounds_table.join(
                        games_table,
                        rounds_table.c.game_slug == games_table.c.slug
                    ),
                )\
                .where(rounds_table.c.id == round_id)  # noqa: E127
    result = await conn.fetch_one(query=query)
    return result and dict(result)
