#!/usr/bin/env python

#-----------------------------------------------------------------------
# database.py
# Author: Bob Dondero, RD/NA/AG
#-----------------------------------------------------------------------

from sys import argv, stderr, exit
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from schema import Base, Events, EventsParticipants, GroupNames, GroupsMembers
import psycopg2
from psycopg2 import connect
from event import Event
from datetime import datetime, date
from os import environ
import os


#-----------------------------------------------------------------------

ENVIRONMENT_ = os.environ.get('ENVIRONMENT_')
DATABASE_URL = os.environ.get('DATABASE_URL')
database_ = os.environ.get('database_')


# Change necessitated by SQLAlchemy / Heroku
if ENVIRONMENT_ == 'deploy':
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        print("IN DEPLOY POSTGRES ALTER DB NAME")

# Create event and add organizer as accepted 
def create_event(initializer_array):

    try:
        if ENVIRONMENT_ == 'deploy':
            engine = create_engine(DATABASE_URL,
                creator=lambda: psycopg2.connect(DATABASE_URL, sslmode='require'))
        elif ENVIRONMENT_ == 'dev':
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
                                           organizer=initializer_array[6],
                                           capacity=initializer_array[7],
                                           participant_count=1,
                                           skill_level=initializer_array[8])

        session.add(addedEvent)


        ev = (session.query(Events)
            .filter(Events.sport == addedEvent.sport,
                    Events.location == addedEvent.location,
                    Events.event_date == addedEvent.event_date,
                    Events.start_time == addedEvent.start_time,
                    Events.end_time == addedEvent.end_time,
                    Events.visibility == addedEvent.visibility,
                    Events.organizer == addedEvent.organizer,
                    Events.capacity == addedEvent.capacity,
                    Events.participant_count == 1,
                    Events.skill_level == addedEvent.skill_level)
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

# initializer_array: [groupname, member, member, ...]
def create_group(initializer_array, username):
    try:
        if ENVIRONMENT_ == 'deploy':
            engine = create_engine(DATABASE_URL,
                creator=lambda: psycopg2.connect(DATABASE_URL, sslmode='require'))
        elif ENVIRONMENT_ == 'dev':
            engine = create_engine('postgresql+psycopg2://@5432/tigerballdb',
            creator=lambda: psycopg2.connect(database='tigerballdb',
                port=5432))
        
        Session = sessionmaker(bind=engine)
        session = Session()

        print(initializer_array)

        addedGroup = GroupNames(group_name=initializer_array[0])

        session.add(addedGroup)

        print("ADDED GROUP")

        gp = (session.query(GroupNames)
            .filter(GroupNames.group_name == addedGroup.group_name)
            .order_by(GroupNames.group_id.desc()).first())

        print("gp")

        addedMember = GroupsMembers(group_id =
            gp.group_id, member_id = username)

        session.add(addedMember)

        # consider checking for repeats to ensure no double-counting
        for mem in initializer_array[1:]:
            addedMember = GroupsMembers(group_id = gp.group_id, member_id = mem)
            session.add(addedMember)
        
        session.commit()
        

        session.close()
        engine.dispose()

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

# see the groups you're in, returns [[gpid, gpname], ...]
def view_groups(username):
    try:
        if ENVIRONMENT_ == 'deploy':
            engine = create_engine(DATABASE_URL,
                creator=lambda: psycopg2.connect(DATABASE_URL, sslmode='require'))
        elif ENVIRONMENT_ == 'dev':
            engine = create_engine('postgresql+psycopg2://@5432/tigerballdb',
            creator=lambda: psycopg2.connect(database='tigerballdb',
                port=5432))

        Session = sessionmaker(bind=engine)
        session = Session()

        groups = session.query(GroupNames).join(GroupsMembers, GroupNames.group_id == GroupsMembers.group_id).\
            filter(GroupsMembers.member_id == username).\
            order_by(GroupNames.group_id.desc()).all()

        returnGroups = []
        for group in groups:
            lst = [group.group_id, group.group_name]
            returnGroups.append(lst)
        
        session.close()
        engine.dispose()
        
        return returnGroups
          

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

# see group name and who's in the group
def get_group_details(group_id):
    try:
        if ENVIRONMENT_ == 'deploy':
            engine = create_engine(DATABASE_URL,
                creator=lambda: psycopg2.connect(DATABASE_URL, sslmode='require'))
        elif ENVIRONMENT_ == 'dev':
            engine = create_engine('postgresql+psycopg2://@5432/tigerballdb',
            creator=lambda: psycopg2.connect(database='tigerballdb',
                port=5432))

        Session = sessionmaker(bind=engine)
        session = Session()

        groupdets = []

        # search for event in events and get the details, add them to array
        gp = (session.query(GroupNames).
            filter(GroupNames.group_id == group_id).one())

        groupdets.append(gp.group_name)

        memsQuery = (session.query(GroupsMembers).
            filter(GroupsMembers.group_id == group_id).all())
        for mem in memsQuery:
            groupdets.append(mem.member_id)

        session.commit()

        session.close()
        engine.dispose()

        return groupdets

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

# add netids to group, no double counting
def add_to_group(group_id, netids):
    try:
        if ENVIRONMENT_ == 'deploy':
            engine = create_engine(DATABASE_URL,
                creator=lambda: psycopg2.connect(DATABASE_URL, sslmode='require'))
        elif ENVIRONMENT_ == 'dev':
            engine = create_engine('postgresql+psycopg2://@5432/tigerballdb',
            creator=lambda: psycopg2.connect(database='tigerballdb',
                port=5432))

        Session = sessionmaker(bind=engine)
        session = Session()

        for netid in netids:
            exists = (session.query(GroupsMembers).
                filter(GroupsMembers.group_id == group_id).
                filter(GroupsMembers.member_id == netid).all())
            if len(exists) == 0:
                newRow = GroupsMembers(group_id=group_id, member_id=netid)
                session.add(newRow)

        session.commit()

        session.close()
        engine.dispose()

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

# leave the group
def leave_group(group_id, username):
    print('not implemented in app.py yet')
    try:
        if ENVIRONMENT_ == 'deploy':
            engine = create_engine(DATABASE_URL,
                creator=lambda: psycopg2.connect(DATABASE_URL, sslmode='require'))
        elif ENVIRONMENT_ == 'dev':
            engine = create_engine('postgresql+psycopg2://@5432/tigerballdb',
            creator=lambda: psycopg2.connect(database='tigerballdb',
                port=5432))

        Session = sessionmaker(bind=engine)
        session = Session()

        gms_to_delete = (session.query(GroupsMembers)
                        .filter(GroupsMembers.group_id == group_id)
                        .filter(GroupsMembers.member_id == username).all())
        for gm in gms_to_delete:
            session.delete(gm)

        session.commit()
        session.close()
        engine.dispose()

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

def update_event(args_arr):
    try:
        if ENVIRONMENT_ == 'deploy':
            engine = create_engine(DATABASE_URL,
                creator=lambda: psycopg2.connect(DATABASE_URL, sslmode='require'))
        elif ENVIRONMENT_ == 'dev':
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
        ev.skill_level = args_arr[3]
        ev.event_date = args_arr[4]
        ev.start_time = args_arr[5]
        ev.end_time = args_arr[6]
        ev.capacity = args_arr[7]
        ev.visibility = args_arr[8]
        
        session.commit()
        session.close()
        engine.dispose()

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

def delete_old_events():
    try:
        if ENVIRONMENT_ == 'deploy':
            engine = create_engine(DATABASE_URL,
                creator=lambda: psycopg2.connect(DATABASE_URL, sslmode='require'))
        elif ENVIRONMENT_ == 'dev':
            engine = create_engine('postgresql+psycopg2://@5432/tigerballdb',
            creator=lambda: psycopg2.connect(database='tigerballdb',
                port=5432))

        Session = sessionmaker(bind=engine)
        session = Session()
        
        events_to_delete = (session.query(Events)
                .filter(Events.event_date < date.today()))
            

        for event in events_to_delete:
            session.delete(event)

        session.commit()
        session.close()
        engine.dispose()

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

def delete_todays_old_events():
    try:
        if ENVIRONMENT_ == 'deploy':
            engine = create_engine(DATABASE_URL,
                creator=lambda: psycopg2.connect(DATABASE_URL, sslmode='require'))
        elif ENVIRONMENT_ == 'dev':
            engine = create_engine('postgresql+psycopg2://@5432/tigerballdb',
            creator=lambda: psycopg2.connect(database='tigerballdb',
                port=5432))
        
        Session = sessionmaker(bind=engine)
        session = Session()

        events_to_delete = (session.query(Events)
            .filter(and_(Events.event_date == date.today(),
            Events.end_time < datetime.now().time())))

        for event in events_to_delete:
            session.delete(event)
        
        session.commit()
        session.close()
        engine.dispose()

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)
        

            

def search_event(args_arr):
    try:
        if ENVIRONMENT_ == 'deploy':
            engine = create_engine(DATABASE_URL,
                creator=lambda: psycopg2.connect(DATABASE_URL, sslmode='require'))
        elif ENVIRONMENT_ == 'dev':
            engine = create_engine('postgresql+psycopg2://@5432/tigerballdb',
            creator=lambda: psycopg2.connect(database='tigerballdb',
                port=5432))

        Session = sessionmaker(bind=engine)
        session = Session()

        all_filters = []
        # conditional sport
        if args_arr[0]:
            all_filters.append(Events.sport == str(args_arr[0]))
        
        # conditional skill level
        if args_arr[1]:
            if str(args_arr[1]) != 'no preference':
                all_filters.append(Events.skill_level == str(args_arr[1]))

        # conditional capacity
        if args_arr[2]:
            all_filters.append(Events.capacity <= int(args_arr[2]))
                
        # conditional event_date
        if args_arr[3]:
            all_filters.append(Events.event_date == str(args_arr[3]))

        # conditional start_time
        if args_arr[4]:
            all_filters.append(Events.start_time >= str(args_arr[4]))
        
        # conditional end_time
        if args_arr[5]:
            all_filters.append(Events.end_time <= str(args_arr[5]))
        
        all_filters.append(Events.visibility == 'public')

        # consider time zones for date and time
        # tz_NY = timezone(timedelta(hours=-4))
        # curr = datetime.now(tz_NY)

        myevents = (session.query(Events)
            .filter(*all_filters).
            # filter(datetime.combine(Events.event_date, Events.end_time) > curr).\
            order_by(Events.event_date).
            order_by(Events.start_time).
            order_by(Events.end_time).all())

        returned_events = []
        for event in myevents:
            return_event = Event([event.event_id, 
                event.sport, event.location, event.event_date,
                event.start_time, event.end_time,
                event.visibility, event.organizer, event.capacity,
                event.participant_count, event.skill_level])
            returned_events.append(return_event)

        session.close()
        engine.dispose()

        return returned_events

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

def search_pending_event(username):
    try:
        if ENVIRONMENT_ == 'deploy':
            engine = create_engine(DATABASE_URL,
                creator=lambda: psycopg2.connect(DATABASE_URL, sslmode='require'))
        elif ENVIRONMENT_ == 'dev':
            engine = create_engine('postgresql+psycopg2://@5432/tigerballdb',
            creator=lambda: psycopg2.connect(database='tigerballdb',
                port=5432))

        Session = sessionmaker(bind=engine)
        session = Session()

        pendingEvents = (session.query(Events).join(EventsParticipants, Events.event_id == EventsParticipants.event_id).
            filter(EventsParticipants.participant_id == username).
            filter(EventsParticipants.participant_status == "no response").
            filter(Events.organizer != username).\
            order_by(Events.event_date).\
            order_by(Events.start_time).\
            order_by(Events.end_time).all())

        returnedPendingEvents = []
        for event in pendingEvents:
            return_event = Event([event.event_id, 
                event.sport, event.location, event.event_date,
                event.start_time, event.end_time,
                event.visibility, event.organizer, event.capacity,
                event.participant_count, event.skill_level])
            returnedPendingEvents.append(return_event)
        
        session.close()
        engine.dispose()
        
        return returnedPendingEvents
          

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

def invite_participant(args_arr):
    try:
        if ENVIRONMENT_ == 'deploy':
            engine = create_engine(DATABASE_URL,
                creator=lambda: psycopg2.connect(DATABASE_URL, sslmode='require'))
        elif ENVIRONMENT_ == 'dev':
            engine = create_engine('postgresql+psycopg2://@5432/tigerballdb',
            creator=lambda: psycopg2.connect(database='tigerballdb',
                port=5432))

        Session = sessionmaker(bind=engine)
        session = Session()

        exists = (session.query(EventsParticipants).
            filter(EventsParticipants.event_id == args_arr[0]).
            filter(EventsParticipants.participant_id == args_arr[1]).all())
        if len(exists) == 0:
            newRow = EventsParticipants(event_id = args_arr[0], participant_id =
                args_arr[1], participant_status = "no response")
            session.add(newRow)
            session.commit()

            session.close()
            engine.dispose()
            return True

        session.close()
        engine.dispose()

        return False


    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

def find_group_id(group_name):
    try:
        if ENVIRONMENT_ == 'deploy':
            engine = create_engine(DATABASE_URL,
                creator=lambda: psycopg2.connect(DATABASE_URL, sslmode='require'))
        elif ENVIRONMENT_ == 'dev':
            engine = create_engine('postgresql+psycopg2://@5432/tigerballdb',
            creator=lambda: psycopg2.connect(database='tigerballdb',
                port=5432))

        Session = sessionmaker(bind=engine)
        session = Session()

        gns = (session.query(GroupNames).
                filter(GroupNames.group_name == group_name).all())

        if len(gns) == 0:
            gid = None
        else:
            gid = gns[0].group_id

        session.commit()

        session.close()
        engine.dispose()

        return gid

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

# gid is the group id
def invite_group(event_id, gid):
    try:
        if ENVIRONMENT_ == 'deploy':
            engine = create_engine(DATABASE_URL,
                creator=lambda: psycopg2.connect(DATABASE_URL, sslmode='require'))
        elif ENVIRONMENT_ == 'dev':
            engine = create_engine('postgresql+psycopg2://@5432/tigerballdb',
            creator=lambda: psycopg2.connect(database='tigerballdb',
                port=5432))

        Session = sessionmaker(bind=engine)
        session = Session()

        print('GOT TO PART 1')
        memsToAdd = (session.query(GroupsMembers).
                filter(GroupsMembers.group_id == gid).all())
        print('GOT TO PART 2')
        print(len(memsToAdd))
        memsToReturn = []
        for mem in memsToAdd:
            print('2.5')
            exists = (session.query(EventsParticipants).
                filter(EventsParticipants.event_id == event_id).
                filter(EventsParticipants.participant_id == mem.member_id).all())
            print('GOT TO PART 3')
            if len(exists) == 0:
                newRow = EventsParticipants(event_id = event_id, participant_id =
                    mem.member_id, participant_status = "no response")
                session.add(newRow)
                memsToReturn.append(mem.member_id)
                print('GOT TO PART 4')


        session.commit()

        session.close()
        engine.dispose()

        return memsToReturn

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

def update_participant(eventid, username, status):
    try:
        if ENVIRONMENT_ == 'deploy':
            engine = create_engine(DATABASE_URL,
                creator=lambda: psycopg2.connect(DATABASE_URL, sslmode='require'))
        elif ENVIRONMENT_ == 'dev':
            engine = create_engine('postgresql+psycopg2://@5432/tigerballdb',
            creator=lambda: psycopg2.connect(database='tigerballdb',
                port=5432))
                
        Session = sessionmaker(bind=engine)
        session = Session()

        participant = (session.query(EventsParticipants).
        	filter(EventsParticipants.event_id == eventid).
            filter(EventsParticipants.participant_id == username).first())

        evToUpdate = (session.query(Events).
                filter(Events.event_id == eventid).one())

        if participant == None:
            print("participant not found")
            newRow = EventsParticipants(event_id = eventid, participant_id = 
        	    username, participant_status = status)
            session.add(newRow)
            if status == 'accepted':
                evToUpdate.participant_count += 1

        else:
            oldStatus = participant.participant_status
            if oldStatus == 'accepted':
                oldNum = 1
            else:
                oldNum = 0
            if status == 'accepted':
                newNum = 1
            else:
                newNum = 0
            participant.participant_status = status
            evToUpdate.participant_count += (newNum - oldNum)

        
        session.commit()
        session.close()
        engine.dispose()

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)


# Returns [ [details] , [participants] ]
def get_details(event_id):
    try:
        if ENVIRONMENT_ == 'deploy':
            engine = create_engine(DATABASE_URL,
                creator=lambda: psycopg2.connect(DATABASE_URL, sslmode='require'))
        elif ENVIRONMENT_ == 'dev':
            engine = create_engine('postgresql+psycopg2://@5432/tigerballdb',
            creator=lambda: psycopg2.connect(database='tigerballdb',
                port=5432))

        Session = sessionmaker(bind=engine)
        session = Session()

        details = []

        print(event_id)

        # search for event in events and get the details, add them to array
        ev = (session.query(Events).
        	filter(Events.event_id == event_id).one())

        details.append(Event([ev.event_id, ev.sport, ev.location, ev.event_date,
        	ev.start_time, ev.end_time, ev.visibility, ev.organizer,
            ev.capacity, ev.participant_count, ev.skill_level]))
  

        # find accepted participants in eventsparticipants
        accepted=[]
        acceptedEventsQuery = (session.query(EventsParticipants).
        	filter(EventsParticipants.event_id == event_id)
            .filter(EventsParticipants.participant_status == 'accepted')
            .all())
        for event in acceptedEventsQuery:
        	accepted.append(event.participant_id)

        declined=[]
        declinedEventsQuery = (session.query(EventsParticipants).
        	filter(EventsParticipants.event_id == event_id)
            .filter(EventsParticipants.participant_status == 'declined')
            .all())  
        for event in declinedEventsQuery:
        	declined.append(event.participant_id)

        undecided=[]
        undecidedEventsQuery = (session.query(EventsParticipants).
        	filter(EventsParticipants.event_id == event_id)
            .filter(EventsParticipants.participant_status == 'undecided')
            .all())  
        for event in undecidedEventsQuery:
        	undecided.append(event.participant_id)
        
        noresponse=[]
        noresponseEventsQuery = (session.query(EventsParticipants).
        	filter(EventsParticipants.event_id == event_id)
            .filter(EventsParticipants.participant_status == 'no response')
            .all())  
        for event in noresponseEventsQuery:
        	noresponse.append(event.participant_id)

        details.append(accepted)
        details.append(declined)
        details.append(undecided)
        details.append(noresponse)

        # print(details)

        session.commit()

        session.close()
        engine.dispose()   

        return details

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

def get_status_events(username, status):
    partstat = ''
    if status == 'attending':
        partstat = 'accepted'
    elif status == 'uncertain':
        partstat = 'undecided'
    elif status == 'not_attending':
        partstat = 'declined'
    else:
        print('NONE OF THE OPTIONS')
    
    try:
        if ENVIRONMENT_ == 'deploy':
            engine = create_engine(DATABASE_URL,
                creator=lambda: psycopg2.connect(DATABASE_URL, sslmode='require'))
        elif ENVIRONMENT_ == 'dev':
            engine = create_engine('postgresql+psycopg2://@5432/tigerballdb',
            creator=lambda: psycopg2.connect(database='tigerballdb',
                port=5432))

        Session = sessionmaker(bind=engine)
        session = Session()

        events = session.query(Events).join(EventsParticipants, Events.event_id == EventsParticipants.event_id).\
            filter(EventsParticipants.participant_status == partstat).\
            filter(EventsParticipants.participant_id == username).\
            order_by(Events.event_date).\
            order_by(Events.start_time).\
            order_by(Events.end_time).all()

        returnEvents = []
        for event in events:
            return_event = Event([event.event_id, 
                event.sport, event.location, event.event_date,
                event.start_time, event.end_time,
                event.visibility, event.organizer, event.capacity,
                event.participant_count, event.skill_level])
            returnEvents.append(return_event)
            print(event.sport)
            print(event.event_date)
            print(event.start_time)
            print(event.end_time)
            print("NEXT EVENT ")
        
        session.close()
        engine.dispose()
        
        return returnEvents
          

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)