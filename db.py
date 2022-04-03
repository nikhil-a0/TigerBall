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

# Create event and add organizer as accepted 
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

        session.add(addedEvent)

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
            ev.event_id, participant_id = ev.organizer, participant_status = "accepted")
        
        session.add(addedParticipant)
        session.commit()
        

        session.close()
        engine.dispose()

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

def update_event(args_arr):
    try:
        engine = create_engine('postgresql+psycopg2://@5432/tigerballdb',
            creator=lambda: psycopg2.connect(database='tigerballdb',
                port=5432))
        
        Session = sessionmaker(bind=engine)
        session = Session()

        # pass in username


        ev = (session.query(Events)
            .filter(Events.event_id == args_arr[0])
            .one())
        ev.sport = args_arr[1]
        ev.location = args_arr[2]
        ev.event_date = args_arr[3]
        ev.start_time = args_arr[4]
        ev.end_time = args_arr[5]
        ev.visibility = args_arr[6]
        ev.organizer = args_arr[7]
        
        session.commit()
        

        session.close()
        engine.dispose()

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

# def delete_event(event_id):
#     try:
#         engine = create_engine('postgresql+psycopg2://@5432/tigerballdb',
#             creator=lambda: psycopg2.connect(database='tigerballdb',
#                 port=5432))  

#     except Exception as ex:
#         print(ex, file=stderr)
#         exit(1)

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
            all_filters.append(Events.start_time >= str(args_arr[3]))
        
        # conditional end_time
        if args_arr[4]:
            all_filters.append(Events.end_time <= str(args_arr[4]))

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

        session.close()
        engine.dispose()

        return returned_events

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

def search_pending_event(username):
    try:
        engine = create_engine('postgresql+psycopg2://@5432/tigerballdb',
            creator=lambda: psycopg2.connect(database='tigerballdb',
                port=5432))

        Session = sessionmaker(bind=engine)
        session = Session()

        pendingEvents = session.query(Events).join(EventsParticipants, Events.event_id == EventsParticipants.event_id).\
            filter(EventsParticipants.participant_status == "no response").\
            filter(Events.organizer != username).all()

        returnedPendingEvents = []
        for event in pendingEvents:
            return_event = Event([event.event_id, 
                event.sport, event.location, event.event_date,
                event.start_time, event.end_time,
                event.visibility, event.organizer])
            returnedPendingEvents.append(return_event)
        
        session.close()
        engine.dispose()
        
        return returnedPendingEvents
          

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

def add_participant(args_arr):
    try:
        engine = create_engine('postgresql+psycopg2://@5432/tigerballdb',
            creator=lambda: psycopg2.connect(database='tigerballdb',
                port=5432))

        Session = sessionmaker(bind=engine)
        session = Session()

        newRow = EventsParticipants(event_id = args_arr[0], participant_id = 
        	args_arr[1], participant_status = "no response")
        session.add(newRow)

        session.commit()

        session.close()
        engine.dispose()

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

def update_participant(eventid, username, status):
    try:
        engine = create_engine('postgresql+psycopg2://@5432/tigerballdb',
            creator=lambda: psycopg2.connect(database='tigerballdb',
                port=5432))
        print("eventid: " + str(eventid))
        print("username:---" + str(username) + "---")
        print("status: " + str(status))

        Session = sessionmaker(bind=engine)
        session = Session()

        participant = (session.query(EventsParticipants).
        	filter(EventsParticipants.event_id == eventid).
            filter(EventsParticipants.participant_id == username).one())

        participant.participant_status = status
        
        session.commit()
        session.close()
        engine.dispose()

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)


# Returns [ [details] , [participants] ]
def get_details(event_id):
    try:
        engine = create_engine('postgresql+psycopg2://@5432/tigerballdb',
            creator=lambda: psycopg2.connect(database='tigerballdb',
                port=5432))
        print('ENGINE CREATED')

        Session = sessionmaker(bind=engine)
        session = Session()

        details = []

        print(event_id)

        # search for event in events and get the details, add them to array
        ev = (session.query(Events).
        	filter(Events.event_id == event_id).one())
        details.append([ev.sport, ev.location, ev.event_date,
        	ev.start_time, ev.end_time, ev.visibility, ev.organizer])

        # find all participants in eventsparticipants
        evps = (session.query(EventsParticipants).
        	filter(EventsParticipants.event_id == event_id).all())
        parts = []
        for evp in evps:
        	parts.append(evp.participant_id)
        details.append(parts)

        session.commit()

        session.close()
        engine.dispose()   

        return details

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

def get_yes_events(username):
    try:
        engine = create_engine('postgresql+psycopg2://@5432/tigerballdb',
            creator=lambda: psycopg2.connect(database='tigerballdb',
                port=5432))

        Session = sessionmaker(bind=engine)
        session = Session()

        events = session.query(Events).join(EventsParticipants, Events.event_id == EventsParticipants.event_id).\
            filter(EventsParticipants.participant_status == "accepted").\
            filter(EventsParticipants.participant_id == username).all()

        returnEvents = []
        for event in events:
            return_event = Event([event.event_id, 
                event.sport, event.location, event.event_date,
                event.start_time, event.end_time,
                event.visibility, event.organizer])
            returnEvents.append(return_event)
        
        session.close()
        engine.dispose()
        
        return returnEvents
          

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

def get_no_events(username):
    try:
        engine = create_engine('postgresql+psycopg2://@5432/tigerballdb',
            creator=lambda: psycopg2.connect(database='tigerballdb',
                port=5432))

        Session = sessionmaker(bind=engine)
        session = Session()

        events = session.query(Events).join(EventsParticipants, Events.event_id == EventsParticipants.event_id).\
            filter(EventsParticipants.participant_status == "declined").\
            filter(EventsParticipants.participant_id == username).all()

        returnEvents = []
        for event in events:
            return_event = Event([event.event_id, 
                event.sport, event.location, event.event_date,
                event.start_time, event.end_time,
                event.visibility, event.organizer])
            returnEvents.append(return_event)
        
        session.close()
        engine.dispose()
        
        return returnEvents
          

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

def get_maybe_events(username):
    try:
        engine = create_engine('postgresql+psycopg2://@5432/tigerballdb',
            creator=lambda: psycopg2.connect(database='tigerballdb',
                port=5432))

        Session = sessionmaker(bind=engine)
        session = Session()

        events = session.query(Events).join(EventsParticipants, Events.event_id == EventsParticipants.event_id).\
            filter(EventsParticipants.participant_status == "undecided").\
            filter(EventsParticipants.participant_id == username).all()

        returnEvents = []
        for event in events:
            return_event = Event([event.event_id, 
                event.sport, event.location, event.event_date,
                event.start_time, event.end_time,
                event.visibility, event.organizer])
            returnEvents.append(return_event)
        
        session.close()
        engine.dispose()
        
        return returnEvents
          

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)
