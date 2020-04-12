from sqlalchemy import Table, Column, String, Text, Integer, DateTime, ForeignKey
from .conn import metadata


users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(64), nullable=False, unique=True, index=True),
    Column("password_hash", String(128), nullable=False),
    Column("gravatar_hash", String(128), nullable=True),
    Column("play_token", String(36), nullable=False),
    Column("play_token_expires_at", DateTime, nullable=False),
    Column("total_score", Integer, server_default="0"),
)


games_table = Table(
    "games",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(64), nullable=False),
    Column("icon", String(32), nullable=True),
    Column("slug", String(64), nullable=False, unique=True, index=True),
    Column("description", Text(), server_default=""),
    Column("idx", Integer),
)


rounds_table = Table(
    "rounds",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("played_at", DateTime, nullable=False),
    Column("game_slug", ForeignKey("games.slug"), nullable=False),
    Column("user_username", ForeignKey("users.username"), nullable=True),
    Column("score", Integer, server_default="0"),
    Column("message", String(128), server_default=""),
    Column("snapshot", Text, nullable=True, server_default=None),
)
