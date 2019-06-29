import sqlalchemy

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
