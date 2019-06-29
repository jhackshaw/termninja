import os

DATABASE_USER = os.environ.get('POSTGRES_USER', 'termninja')
DATABASE_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'testing')
DATABASE_NAME = os.environ.get('POSTGRES_DB', 'termninja')
DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@postgres/{DATABASE_NAME}"

PORT = os.environ.get('PUBLIC_API_PORT', 3000)

