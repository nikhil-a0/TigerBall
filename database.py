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
DATABASE_URL = 'file:database.sqlite?mode=rw'


# add event to database
def add_event(event_data):

    with connect(DATABASE_URL, uri=True) as connection:

        with closing(connection.cursor()) as cursor:
            

def search_event(query_data):

def delete_event(query_data):

def add_profile(profile_data):

