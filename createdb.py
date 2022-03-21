#!/usr/bin/env python

#-----------------------------------------------------------------------
# createdb.py
# Author: Bob Dondero, NA/RD/AG
#-----------------------------------------------------------------------

from sys import argv, stderr, exit
import psycopg2
from psycopg2 import connect

#-----------------------------------------------------------------------

def main():

    if len(argv) != 1:
        print('Usage: python createdb.py', file=stderr)
        exit(1)

    try:
        conn = psycopg2.connect(database='postgres',
            port=5432)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute("DROP DATABASE IF EXISTS tigerballdb")
        cursor.execute("CREATE DATABASE tigerballdb")

        with connect(
            host='localhost', port=5432,
            database='tigerballdb') as connection:

            with connection.cursor() as cursor:

                #-------------------------------------------------------

                cursor.execute("DROP TABLE IF EXISTS events")
                cursor.execute("CREATE TABLE events "
                    + "(event_id SERIAL NOT NULL, sport TEXT, location TEXT,"
                    + " event_date DATE, start_time TIME, end_time TIME, "
                    "visibility TEXT, organizer_id TEXT)")

                #-------------------------------------------------------

                cursor.execute("DROP TABLE IF EXISTS eventsparticipants")
                cursor.execute("CREATE TABLE eventsparticipants "
                    + "(event_id INTEGER, participant_id TEXT)")

                #-------------------------------------------------------

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
