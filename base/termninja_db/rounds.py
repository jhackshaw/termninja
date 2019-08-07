import datetime
from sqlalchemy import (insert,
                        select)
from .conn import conn
from .tables import rounds_table, games_table, users_table


PAGE_SIZE = 10

list_columns = [
    rounds_table.c.id,
    rounds_table.c.played_at,
    rounds_table.c.score,
    rounds_table.c.result_message,
    games_table.c.server_name,
    games_table.c.slug,
    users_table.c.username,
    users_table.c.gravatar_hash
]

detail_columns = list_columns + [
    rounds_table.c.result_snapshot
]

select_from_default = \
    rounds_table\
        .join(
            games_table,
            rounds_table.c.game_slug == games_table.c.slug
        )\
        .join(
            users_table,
            rounds_table.c.user_username == users_table.c.username
        )  # noqa: E127


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
    """
    List PAGE_SIZE rounds for the supplied filters.
    Join users_table and games_table.
    """
    where_clause = [
        getattr(rounds_table.c, k) == v
        for k, v in filters.items()
    ]
    # join user?
    query = select(list_columns)\
                .select_from(select_from_default)\
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


async def list_high_scores(**filters):
    """
    List top 10 rounds with the highest score for the
    given filters
    """
    where_clause = [
        getattr(rounds_table.c, k) == v
        for k, v in filters.items()
    ]
    query = select(list_columns)\
                .select_from(select_from_default)\
                .where(*where_clause)\
                .order_by(rounds_table.c.score.desc())\
                .limit(10)   # noqa: E127
    result = await conn.fetch_all(query=query)
    return result and [
        dict(r) for r in result
    ]


async def get_round_details(round_id):
    """
    Get details for a given round (include snapshot)
    """
    query = select(detail_columns)\
                .select_from(select_from_default)\
                .where(rounds_table.c.id == round_id)  # noqa: E127
    result = await conn.fetch_one(query=query)
    return result and dict(result)
