#-----------------------------------------------------------------------
# event.py
# Author: Nikhil Ajjarapu
#-----------------------------------------------------------------------
class Event:

    def __init__(self, initializer_array):
        self._event_id = initializer_array[0]
        self._sport = initializer_array[1]
        self._location =  initializer_array[2]
        self._date = initializer_array[3].strftime('%-m/%-d')
        self._starttime = initializer_array[4].strftime('%I:%M %p')
        self._endtime = initializer_array[5].strftime('%I:%M %p')
        self._visibility = initializer_array[6]
        self._organizer = initializer_array[7]
        self._capacity = initializer_array[8]
        self._participant_count = initializer_array[9]
        self._skill_level = initializer_array[10]
        
    def get_event_id(self):
        return self._event_id

    def get_sport(self):
        return self._sport

    def get_location(self):
        return self._location

    def get_date(self):
        return self._date
    
    def get_starttime(self):
        return self._starttime
    
    def get_endtime(self):
        return self._endtime
    
    def get_visibility(self):
        return self._visibility

    def get_organizer(self):
        return self._organizer

    def get_capacity(self):
        return self._capacity
    
    def get_participant_count(self):
        return self._participant_count
    
    def get_skill_level(self):
        return self._skill_level
