#!/usr/bin/env python

#-----------------------------------------------------------------------
# database.py
# Author: Bob Dondero, RD/NA/AG
#-----------------------------------------------------------------------

from sys import argv, stderr, exit
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from schema import Base, Events, EventsParticipants
import psycopg2
from psycopg2 import connect
from event import Event

#-----------------------------------------------------------------------

def create_event(initializer_array):

    try:
        engine = create_engine('postgresql+psycopg2://@5432/tigerballdb',
            creator=lambda: psycopg2.connect(database='tigerballdb',
                port=5432))
        
        Session = sessionmaker(bind=engine)
        session = Session()

        addedEvent = Events(                    sport=initializer_array[0],
                                           location=initializer_array[1],
                                           event_date=initializer_array[2],
                                           start_time=initializer_array[3],
                                           end_time=initializer_array[4],
                                           visibility=initializer_array[5],
                                           organizer=initializer_array[6])

        print("CREATED NEW EVENT TO ADD")
        session.add(addedEvent)
        print("ADDED EVENT TO SESSION")

        # statement = Events.insert().values(sport=initializer_array[0],
        #                                    location=initializer_array[1],
        #                                    event_date=initializer_array[2],
        #                                    start_time=initializer_array[3],
        #                                    end_time=initializer_array[4],
        #                                    visibility=initializer_array[5])


        ev = (session.query(Events)
            .filter(Events.sport == addedEvent.sport,
                    Events.location == addedEvent.location,
                    Events.event_date == addedEvent.event_date,
                    Events.start_time == addedEvent.start_time,
                    Events.end_time == addedEvent.end_time,
                    Events.visibility == addedEvent.visibility,
                    Events.organizer == Events.organizer)
            .one())

        addedParticipant = EventsParticipants(event_id =
            ev.event_id, participant_id = ev.organizer)
        
        session.add(addedParticipant)
        session.commit()
        
        #engine.execute(statement)

        session.close()
        engine.dispose()
        # print("DISPOSED")

        # event = Event(initializer_array)
        # print("EVENT TO RETURN")

        # return event



#     try:
#         with connect(
#             host='localhost', port=5432,
#             database='tigerballdb') as connection:

#             with connection.cursor() as cursor:

#                 # Create a prepared statement and substitute values.
#                 stmt_str = 'INSERT INTO events (sport, location, event_date, start_time, \
#                 end_time, visibility, organizer_id) \
#                 VALUES (%s, %s, %s, %s, %s, %s, %s)'
#                 cursor.execute(stmt_str, initializer_array)
#                 print("INSERTED")

#                 stmt_str = 'SELECT event_id FROM events WHERE \
#                 events.sport = %s AND events.location = %s AND \
#                 events.event_date = %s AND events.start_time = %s AND \
#                 events.end_time = %s AND events.visibility = %s AND \
#                 events.organizer_id = %s'
#                 cursor.execute(stmt_str, initializer_array)
#                 row = cursor.fetchone()
#                 # only taking one (later make statement that deletes duplicates)
#                 event_id = str(row[0])

#                 stmt_str = 'SELECT event_id, sport FROM events'
#                 cursor.execute(stmt_str)
#                 row = cursor.fetchone()
#                 print("FETCHED")
#                 print(row)
#                 event_id = str(row[0])
#                 print(str(row[0]) + " " + str(row[1]))

#                 stmt_str = 'INSERT INTO eventsparticipants (event_id, participant_id) \
#                 VALUES (' + str(event_id) + ', %s)'
#                 cursor.execute(stmt_str, [initializer_array[6]])

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

def search_event(args_arr):
    try:
        engine = create_engine('postgresql+psycopg2://@5432/tigerballdb',
            creator=lambda: psycopg2.connect(database='tigerballdb',
                port=5432))
        
        Session = sessionmaker(bind=engine)
        session = Session()

        all_filters = []
        # conditional sport
        if args_arr[0]:
            all_filters.append(Events.sport == str(args_arr[0]))
        
        # conditional location
        if args_arr[1]:
            all_filters.append(Events.location == str(args_arr[1]))
        
        # conditional event_date
        if args_arr[2]:
            all_filters.append(Events.event_date == str(args_arr[2]))

        # conditional start_time
        if args_arr[3]:
            all_filters.append(Events.start_time == str(args_arr[3]))
        
        # conditional end_time
        if args_arr[4]:
            all_filters.append(Events.end_time == str(args_arr[4]))

        # conditional visibility
        if args_arr[5]:
            all_filters.append(Events.visibility == str(args_arr[5]))
        
        # conditional organizer
        if args_arr[6]:
            all_filters.append(Events.organizer == str(args_arr[6]))


        myevents = (session.query(Events)
            .filter(*all_filters)
            .all())

        returned_events = []
        for event in myevents:
            return_event = Event([event.event_id, 
                event.sport, event.location, event.event_date,
                event.start_time, event.end_time,
                event.visibility, event.organizer])
            returned_events.append(return_event)


        return returned_events

        # events = (session.query(Events)
        #     .filter())    
                
        #         # Create a prepared statement and substitute values.
        #         stmt_str = 'SELECT events.event_id, events.sport, events.location, events.event_date, \
        #         events.start_time, events.end_time, events.visibility, events.organizer_id \
        #         FROM events WHERE TRUE'
        #         args_list = []

        #         # conditional sport
        #         if args_arr[0]:
        #             stmt_str += " AND sport LIKE %s ESCAPE '\\'"
        #             modified_args_d = args_arr[0].replace("_","\\_")
        #             modified_args_d = modified_args_d.replace("%","\\%")
        #             args_list.append(modified_args_d)

        #         # conditional location
        #         if args_arr[1]:
        #             stmt_str += " AND location LIKE %s ESCAPE '\\'"
        #             modified_args_n = args_arr[1].replace("_","\\_")
        #             modified_args_n = modified_args_n.replace("%","\\%")
        #             args_list.append(modified_args_n)

        #         # conditional event_date
        #         if args_arr[2]:
        #             stmt_str += " AND event_date LIKE %s ESCAPE '\\'"
        #             modified_args_a = args_arr[2].replace("_","\\_")
        #             modified_args_a = modified_args_a.replace("%","\\%")
        #             args_list.append(modified_args_a)

        #         print("Arrived before args_arr[3]")
        #         # conditional start_time
        #         if args_arr[3]:
        #             stmt_str += " AND start_time LIKE %s ESCAPE '\\'"
        #             modified_args_t = args_arr[3].replace("_","\\_")
        #             modified_args_t = modified_args_t.replace("%","\\%")
        #             args_list.append(modified_args_t)

        #         # conditional end_time
        #         if args_arr[4]:
        #             stmt_str += " AND end_time LIKE %s ESCAPE '\\'"
        #             modified_args_t = args_arr[4].replace("_","\\_")
        #             modified_args_t = modified_args_t.replace("%","\\%")
        #             args_list.append(modified_args_t)

        #          # conditional visibility
        #         if args_arr[5]:
        #             stmt_str += " AND visibility LIKE %s ESCAPE '\\'"
        #             modified_args_t = args_arr[5].replace("_","\\_")
        #             modified_args_t = modified_args_t.replace("%","\\%")
        #             args_list.append(modified_args_t)

        #          # conditional organizer_id
        #         if args_arr[6]:
        #             stmt_str += " AND organizer_id LIKE %s ESCAPE '\\'"
        #             modified_args_t = args_arr[6].replace("_","\\_")
        #             modified_args_t = modified_args_t.replace("%","\\%")
        #             args_list.append(modified_args_t)
        #         print("Arrived after args_arr[6]")

        #         stmt_str += ' ORDER BY events.event_date ASC, \
        #                     events.start_time ASC, \
        #                     events.end_time ASC, \
        #                     events.event_id ASC'

        #         cursor.execute(stmt_str, args_list)
        #         print("CURSOR EXECUTED SEARCH")
                
        #         eventList = []

        #         row = cursor.fetchone()
        #         print("Fetched after searching")
        #         print("ROW")
        #         print(row)
        #         while row is not None:
        #             row_arr = [str(row[0]),
        #                 str(row[1]), str(row[2]),
        #                 str(row[3]), str(row[4]),
        #                 str(row[5]), str(row[6]),
        #                 str(row[7])]
        #             eventList.append(Event(row_arr))
        #             row = cursor.fetchone()
                    
        #         print("EVENT LIST SIZE")
        #         print(len(eventList))
                
        #         return eventList

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)
