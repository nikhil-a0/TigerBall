#!/usr/bin/env python

#-----------------------------------------------------------------------
# create.py
# Author: Bob Dondero, RD/NA/AG
#-----------------------------------------------------------------------

from sys import argv, stderr, exit
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from schema import Base, Events, EventsParticipants
import psycopg2
from psycopg2 import connect
import os



#-----------------------------------------------------------------------

def main():
    # Create db locally

    if len(argv) != 1:
        print('Usage: python create.py', file=stderr)
        exit(1)

    try:
        ENVIRONMENT_ = os.environ.get('ENVIRONMENT_')
        DATABASE_URL = os.environ.get('DATABASE_URL')
        database_ = os.environ.get('database_')         
        # conn = psycopg2.connect(database='postgres',
        #     port=5432)
        # conn.autocommit = True
        # cursor = conn.cursor()
        # cursor.execute("DROP DATABASE IF EXISTS tigerballdb")
        # cursor.execute("CREATE DATABASE tigerballdb")
        # print('DATABASE CREATED')

        # engine = create_engine('postgresql+psycopg2://@5432/tigerballdb',
        #     creator=lambda: psycopg2.connect(database='tigerballdb',
        #         port=5432))
        # print('ENGINE CREATED')

        # Session = sessionmaker(bind=engine)
        # session = Session()

        # Base.metadata.drop_all(engine)
        # Base.metadata.create_all(engine)

        # Create db in Heroku
        if DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        engine = create_engine(DATABASE_URL,
            creator=lambda: psycopg2.connect(DATABASE_URL, sslmode='require'))
        
        Session = sessionmaker(bind=engine)
        session = Session()
        print('ENGINE CREATED')

        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        

        #---------------------------------------------------------------

        session.close()
        engine.dispose()

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
