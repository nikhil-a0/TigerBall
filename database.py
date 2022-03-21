#-----------------------------------------------------------------------
# database.py
# Authors: Rishi Dange, Nikhil Ajjarapu
#-----------------------------------------------------------------------

from sys import argv, stderr, exit
from psycopg2 import connect
from event import Event

def create_event(initializer_array):
    try:
        with connect(
            host='localhost', port=5432,
            database='tigerballdb') as connection:

            with connection.cursor() as cursor:

                # Create a prepared statement and substitute values.
                stmt_str = 'INSERT INTO events (sport, location, event_date, start_time, \
                end_time, visibility, organizer_id) \
                VALUES (%s, %s, %s, %s, %s, %s, %s)'
                cursor.execute(stmt_str, initializer_array)

#                 stmt_str = 'SELECT event_id FROM events WHERE \
#                 events.sport = %s AND events.location = %s AND \
#                 events.event_date = %s AND events.start_time = %s AND \
#                 events.end_time = %s AND events.visibility = %s AND \
#                 events.organizer_id = %s'
#                 cursor.execute(stmt_str, initializer_array)
#                 row = cursor.fetchone()
#                 # only taking one (later make statement that deletes duplicates)
#                 event_id = str(row[0])

                stmt_str = 'SELECT event_id, sport FROM events'
                cursor.execute(stmt_str)
                row = cursor.fetchone()
                event_id = str(row[0])
                print(str(row[0]) + " " + str(row[1]))

                stmt_str = 'INSERT INTO eventsparticipants (event_id, participant_id) \
                VALUES (' + str(event_id) + ', %s)'
                cursor.execute(stmt_str, [initializer_array[6]])

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

def search_event(args_arr):
    try:
        with connect(
            host='localhost', port=5432,
            database='tigerballdb') as connection:

            with connection.cursor() as cursor:

                # Create a prepared statement and substitute values.
                stmt_str = 'SELECT events.event_id, events.sport, events.location, events.event_date, \
                events.start_time, events.end_time, events.visibility, events.organizer_id \
                FROM events, eventsparticipants WHERE events.event_id = eventsparticipants.event_id'
                args_list = []

                # conditional sport
                if args_arr[0]:
                    stmt_str += " AND sport LIKE %s ESCAPE '\\'"
                    modified_args_d = args_arr[0].replace("_","\\_")
                    modified_args_d = modified_args_d.replace("%","\\%")
                    args_list.append("%" + modified_args_d + "%")

                # conditional location
                if args_arr[1]:
                    stmt_str += " AND location LIKE ? ESCAPE '\\'"
                    modified_args_n = args_arr[1].replace("_","\\_")
                    modified_args_n = modified_args_n.replace("%","\\%")
                    args_list.append("%" + modified_args_n + "%")

                # conditional event_date
                if args_arr[2]:
                    stmt_str += " AND event_date LIKE ? ESCAPE '\\'"
                    modified_args_a = args_arr[2].replace("_","\\_")
                    modified_args_a = modified_args_a.replace("%","\\%")
                    args_list.append("%" + modified_args_a + "%")

                # conditional start_time
                if args_arr[3]:
                    stmt_str += " AND start_time LIKE ? ESCAPE '\\'"
                    modified_args_t = args_arr[3].replace("_","\\_")
                    modified_args_t = modified_args_t.replace("%","\\%")
                    args_list.append("%" + modified_args_t + "%")

                # conditional end_time
                if args_arr[4]:
                    stmt_str += " AND end_time LIKE ? ESCAPE '\\'"
                    modified_args_t = args_arr[4].replace("_","\\_")
                    modified_args_t = modified_args_t.replace("%","\\%")
                    args_list.append("%" + modified_args_t + "%")

                 # conditional visibility
                if args_arr[5]:
                    stmt_str += " AND visibility LIKE ? ESCAPE '\\'"
                    modified_args_t = args_arr[5].replace("_","\\_")
                    modified_args_t = modified_args_t.replace("%","\\%")
                    args_list.append("%" + modified_args_t + "%")

                 # conditional organizer_id
                if args_arr[6]:
                    stmt_str += " AND organizer_id LIKE ? ESCAPE '\\'"
                    modified_args_t = args_arr[6].replace("_","\\_")
                    modified_args_t = modified_args_t.replace("%","\\%")
                    args_list.append("%" + modified_args_t + "%")


                stmt_str += ' ORDER BY events.event_date ASC, \
                            events.start_time ASC, \
                            events.end_time ASC, \
                            events.event_id ASC'

                cursor.execute(stmt_str, args_list)

                eventList = []

                row = cursor.fetchone()
                while row is not None:
                    row_arr = [str(row[0]),
                        str(row[1]), str(row[2]),
                        str(row[3]), str(row[4]),
                        str(row[5]), str(row[6])]
                    answer.append(Event(row_arr))
                    row = cursor.fetchone()
                
                return eventList

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)
