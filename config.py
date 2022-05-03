import os
import re

# dev or deploy

ENVIRONMENT_ = os.environ.get('ENVIRONMENT_')
DATABASE_URL = os.environ.get('DATABASE_URL')
database_ = os.environ.get('database_')
USERNAME_ = 'normal'

if ENVIRONMENT_ == 'dev':
    DATABASE_URL = 'postgresql+psycopg2://@5432/tigerballdb'
    database_ = 'tigerballdb'
elif ENVIRONMENT_ == 'deploy':
    DATABASE_URL = os.getenv("DATABASE_URL")  # or other relevant config var
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        database_ = ''


# normal or whatever username you want
USERNAME_ = 'TEST'

