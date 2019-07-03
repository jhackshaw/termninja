from .db import db, metadata, DATABASE_URL

# these need to import here in order to attach to metadata
from .users import table as users_table