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
from config import USERNAME_, ENVIRONMENT_, DATABASE_URL, database_


#-----------------------------------------------------------------------

def main():

    if len(argv) != 1:
        print('Usage: python create.py', file=stderr)
        exit(1)

    try:
        # conn = psycopg2.connect(database='postgresql',
        #     port=5432)
        # conn.autocommit = True
        # cursor = conn.cursor()
        # cursor.execute("DROP DATABASE IF EXISTS d5olnm6egr5314")
        # cursor.execute("CREATE DATABASE d5olnm6egr5314")
        # print('DATABASE CREATED')

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
