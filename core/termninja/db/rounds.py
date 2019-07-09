import datetime
from sqlalchemy import (insert,
                        select)
from .conn import conn
from .tables import rounds_table


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
