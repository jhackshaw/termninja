import os
import sqlalchemy
from databases import Database

metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    'users',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('username', sqlalchemy.String(length=64)),
)

games = sqlalchemy.Table(
    'games',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('name', sqlalchemy.String(length=100)),
    sqlalchemy.Column('port', sqlalchemy.Integer()),
    sqlalchemy.Column('command', sqlalchemy.String(length=120))
)


DATABASE_USER = os.environ.get('POSTGRES_USER', 'termninja')
DATABASE_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'testing')
DATABASE_NAME = os.environ.get('POSTGRES_DB', 'termninja')
DATABASE_HOST = os.environ.get('POSTGRES_HOST', 'postgres')
DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"

db = Database(DATABASE_URL)
