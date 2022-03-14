#-----------------------------------------------------------------------
# event.py
# Author: Nikhil Ajjarapu
#-----------------------------------------------------------------------

class Event:

    def __init__(self, sport, location, datetime):
        self.sport = sport
        self.location = location
        self.datetime = datetime

    def __str__(self):
        return self.sport + ', ' + self.location + ', ' + self.datetime

    def getSport(self):
        return self.sport

    def getLocation(self):
        return self.location

    def getDatetime(self):
        return self.datetime