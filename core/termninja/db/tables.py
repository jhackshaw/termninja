from sqlalchemy import (Table,
                        Column,
                        String,
                        Text,
                        Integer,
                        DateTime,
                        ForeignKey)
from .conn import metadata


users_table = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(64), nullable=False, unique=True, index=True),
    Column('password_hash', String(128), nullable=False),
    Column('play_token', String(36), nullable=False),
    Column('play_token_expires_at', DateTime, nullable=False),
    Column('score', Integer, server_default='0')
)

#
# represents an instance of a running (or unresponsive) game
#
games_table = Table(
    'games',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('friendlyname', String(64), nullable=False, unique=True, index=True),
    Column('port', Integer),
    Column('last_active', DateTime, nullable=False)
)

#
# represents a single play of a game by a user
#
rounds_table = Table(
    'rounds',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('played_at', DateTime, nullable=False),
    Column('game_friendlyname', ForeignKey('games.friendlyname'), nullable=False),
    Column('user_username', ForeignKey('users.username'), nullable=True), # null user = anonymous user
    Column('score', Integer, server_default='0'),
    Column('result_message', String(128), server_default=''),
    Column('result_snapshot', Text, nullable=True, server_default=None)
)

