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

#-----------------------------------------------------------------------

def main():

    if len(argv) != 1:
        print('Usage: python create.py', file=stderr)
        exit(1)

    try:
        conn = psycopg2.connect(database='postgresql',
            port=5432)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute("DROP DATABASE IF EXISTS d5olnm6egr5314")
        cursor.execute("CREATE DATABASE d5olnm6egr5314")
        print('DATABASE CREATED')

        engine = create_engine('postgres://fjoacapxjmfqdq:6bc7c2106fefb7d79382461eaa98fe8cab9b686892fd9022c20abcfd88ace07c@ec2-34-207-12-160.compute-1.amazonaws.com:5432/d5olnm6egr5314',
            creator=lambda: psycopg2.connect(database='d5olnm6egr5314',
                port=5432))
        print('ENGINE CREATED')

        Session = sessionmaker(bind=engine)
        session = Session()

        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        #---------------------------------------------------------------

#         event = Events(sport='soccer', location='poe', event_date='2022-03-21',
#             start_time='14:30:00', end_time='15:30:00', visibility='public',
#             organizer='rdange')
#         session.add(event)
#         session.commit()
#         print('FAKE EVENT ADDED')

        #---------------------------------------------------------------

        session.close()
        engine.dispose()

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
