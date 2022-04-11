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
from config import USERNAME_, ENVIRONMENT_, DATABASE_URL


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
            creator=lambda: psycopg2.connect(database=database_,
                port=5432))
        print('ENGINE CREATED')

        Session = sessionmaker(bind=engine)
        session = Session()

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
