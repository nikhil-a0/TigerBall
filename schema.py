# schema.py

#!/usr/bin/env python

#--------
# schema.py
# Author: RD, NA, AG
#--------

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Time

Base = declarative_base()

class Events (Base):
	__tablename__ = 'events'
	event_id = Column(Integer, primary_key=True, autoincrement=True)
	sport = Column(String)
	location = Column(String)
	event_date = Column(Date)
	start_time = Column(Time)
	end_time = Column(Time)
	visibility = Column(String)
	organizer = Column(String)

class EventsParticipants (Base):
	__tablename__ = 'eventsparticipants'
	ep_id = Column(Integer, primary_key=True, autoincrement=True)
	event_id = Column(Integer)
	participant_id = Column(String)
