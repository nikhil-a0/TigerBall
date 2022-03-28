#!/usr/bin/env python

#-----------------------------------------------------------------------
# create.py
# Author: Bob Dondero, RD/NA/AG
#-----------------------------------------------------------------------

from sys import argv, stderr, exit
from sqlite3 import connect as sqlite_connect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from schema import Base, Events, EventsParticipants
import psycopg2
from psycopg2 import connect

#-----------------------------------------------------------------------

def main():

    if len(argv) != 1:
        print('Usage: python create.py', file=stderr)
        exit(1)

    try:
        conn = psycopg2.connect(database='postgres',
            port=5432)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute("DROP DATABASE IF EXISTS tigerballdb")
        cursor.execute("CREATE DATABASE tigerballdb")
        print('DATABASE CREATED')

        engine = create_engine('postgresql+psycopg2://@5432/tigerballdb',
            creator=lambda: psycopg2.connect(database='tigerballdb',
                port=5432))
        print('ENGINE CREATED')

        Session = sessionmaker(bind=engine)
        session = Session()

        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        #---------------------------------------------------------------

        event = Events(sport='soccer', location='poe', date='2022-03-21',
            start_time='14:30:00', end_time='15:30:00', visibility='public',
            organizer='rdange')
        session.add(event)
        session.commit()

        #---------------------------------------------------------------

        session.close()
        engine.dispose()

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
