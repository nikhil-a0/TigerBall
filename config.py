import os
from os import environ
# dev or deploy

ENVIRONMENT_ = 'deploy'

if ENVIRONMENT_ == 'dev':
    DATABASE_URL = 'postgresql+psycopg2://@5432/tigerballdb'
    database_ = 'tigerballdb'
elif ENVIRONMENT_ == 'deploy':
    DATABASE_URL = environ.get('DATABASE_URL')


# normal or whatever username you want
USERNAME_ = 'lisa'