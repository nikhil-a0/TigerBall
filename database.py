#-----------------------------------------------------------------------
# database.py
# Authors: Arin Mukherjee, Nikhil Ajjarapu
#-----------------------------------------------------------------------

# NOTE: much of this code is copied from courseserver6.py

from os import name
from sys import exit, stderr
from socket import socket, SOL_SOCKET, SO_REUSEADDR
from pickle import dump, load
import argparse
from contextlib import closing
from sqlite3 import connect


#-----------------------------------------------------------------------
DATABASE_URL = 'file:database?mode=rw'


#-----------------------------------------------------------------------
# Formats prepared statements w.r.t wildcard characters

def prep_stmt_format(arg):
    return "%" + str(arg).lower().replace(
        "%", "!%").replace("_","!_") + "%"

#-----------------------------------------------------------------------
# add event to database
# def add_event(event):

#     with connect(DATABASE_URL, uri=True) as connection:

#         with closing(connection.cursor()) as cursor:

            
            

# def delete_event(query_data):

def search_event(query_data):
    events = []
    with connect(DATABASE_URL, uri=True) as connection:

        with closing(connection.cursor()) as cursor:

            stmt_str = "SELECT * FROM events"

            prep_stmts = []

            sport = query_data[0]
            location = query_data[1]
            datetime = query_data[2]

            # Modify query according to command-line args
            if (sport is not None) and (sport.strip() != ''):
                stmt_str += "WHERE LOWER(events.sport) LIKE ? ESCAPE '!' "
                prep_stmts.append(prep_stmt_format(sport))
            if (location is not None) and (location.strip() != ''):
                stmt_str += "AND LOWER(events.location) LIKE ? ESCAPE '!' "
                prep_stmts.append(prep_stmt_format(location))
            if (datetime is not None) and (datetime.strip() != ''):
                stmt_str += "AND LOWER(events.datetime) LIKE ? ESCAPE '!' "
                prep_stmts.append(prep_stmt_format(datetime))

            stmt_str += "ORDER BY events.datetime ASC"

            cursor.execute(stmt_str, prep_stmts)
            row = cursor.fetchone()

            while row is not None:
                events.append(str(row[0]).rjust(5, ' ') + "  " +
                            str(row[1]) + str(row[2]).rjust(7,
                            ' '))
                row = cursor.fetchone()

            return ['not error', events]


# def add_profile(profile_data):

