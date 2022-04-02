#-----------------------------------------------------------------------
# app.py
#-----------------------------------------------------------------------

from time import localtime, asctime, strftime
from flask import Flask, request, make_response, redirect, url_for
from flask import render_template
from keys import APP_SECRET_KEY
from db import search_event, create_event, get_details, add_participant, update_event

#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='.')

app.secret_key = APP_SECRET_KEY

import auth

#-----------------------------------------------------------------------

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    username = auth.authenticate()

    if request.method == 'POST':
        initializer_array = [request.form.get('sport_c'), 
                            request.form.get('location_c'), 
                            request.form.get('date_c'),
                            request.form.get('start_time_c'),
                            request.form.get('end_time_c'),
                            request.form.get('visibility_c'),
                            request.form.get('organizer_id_c')]

        create_event(initializer_array)
        query_data = ['','','','','','','']


    if request.method == 'GET':
        query_data = [request.args.get('sport_f'), 
                    request.args.get('location_f'), 
                    request.args.get('date_f'),
                    request.args.get('start_time_f'),
                    request.args.get('end_time_f'),
                    request.args.get('visibility_f'),
                    request.args.get('organizer_id_f')]
        for i in range(7):
            if query_data[i] is None:
                query_data[i] = ''


    events = search_event(query_data)
    html = render_template('index.html', events = events, username = username)
    response = make_response(html)
    
    return response

#-----------------------------------------------------------------------

@app.route('/eventdetails', methods=['GET', 'POST'])

def event_details():

    username = auth.authenticate()

    event_id = request.args.get('event_id')
    details = get_details(event_id)

    if request.method == 'POST':
            # update 1 participant if added
        participant_id = request.form.get('participant_id')
        if participant_id != None: 
            add_participant([event_id, participant_id])

        initializer_array = [event_id,
                            request.form.get('sport_c'), 
                            request.form.get('location_c'), 
                            request.form.get('date_c'),
                            request.form.get('start_time_c'),
                            request.form.get('end_time_c'),
                            request.form.get('visibility_c'),
                            request.form.get('organizer_id_c')]
        changed = False
        for x in range(1, len(initializer_array)):
            if initializer_array[x] != None:
                changed = True

        if changed == True:
            update_event(initializer_array)
            print("Ran!")
    
    details = get_details(event_id)
    html = render_template('eventdetails.html', details = details, event_id = event_id, username = username)
    response = make_response(html)
    return response
