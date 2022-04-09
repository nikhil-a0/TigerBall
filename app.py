#-----------------------------------------------------------------------
# app.py
#-----------------------------------------------------------------------

from time import localtime, asctime, strftime
from flask import Flask, request, make_response, redirect, url_for
from flask import render_template
from keys import APP_SECRET_KEY
from db import search_event, create_event, get_details, invite_participant,\
    update_event, search_pending_event, update_participant,\
    get_yes_events, get_maybe_events, get_no_events
from config import USERNAME_, ENVIRONMENT_

#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='templates')

if ENVIRONMENT_ == 'deploy':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fjoacapxjmfqdq:6bc7c2106fefb7d79382461eaa98fe8cab9b686892fd9022c20abcfd88ace07c@ec2-34-207-12-160.compute-1.amazonaws.com:5432/d5olnm6egr5314'
    app.debug = False
elif ENVIRONMENT_ == 'dev':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://@5432/tigerballdb'
    app.debug = True

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = APP_SECRET_KEY

import auth

#-----------------------------------------------------------------------

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    print("index")

    if USERNAME_ == 'normal':
        username = auth.authenticate().strip()
    else:
        username = USERNAME_


    # Pending Events

    # pending_events = search_pending_event(username)
    query_data = ['','','','','','','']
    pending_events = query_data
    events = pending_events

    # if request.method == 'GET':
    #     query_data = [request.args.get('sport_f'),
    #                 request.args.get('skill_level_f'),
    #                 request.args.get('capacity_f'),
    #                 request.args.get('date_f'),
    #                 request.args.get('start_time_f'),
    #                 request.args.get('end_time_f')]
    #     for i in range(0, len(query_data)):
    #         if query_data[i] is None:
    #             query_data[i] = ''

    # print("after get")
    # print(pending_events)
    # events = search_event(query_data)
    html = render_template('index-1.html', username = username, pending_events = pending_events, events = events)
    response = make_response(html)
    
    return response

#-----------------------------------------------------------------------
@app.route('/create', methods=['GET','POST'])
def create():
    if USERNAME_ == 'normal':
        username = auth.authenticate().strip()
    else:
        username = USERNAME_

    if request.method == 'POST':
        initializer_array = [request.form.get('sport_c'), 
                            request.form.get('location_c'), 
                            request.form.get('date_c'),
                            request.form.get('start_time_c'),
                            request.form.get('end_time_c'),
                            request.form.get('visibility_c'),
                            username,
                            request.form.get('capacity_c'),
                            request.form.get('skill_level_c')]
        print(initializer_array)
        create_event(initializer_array)
        return redirect(url_for('my_events'))

    
    html = render_template('create.html', username = username)
    response = make_response(html)
    
    return response




@app.route('/register', methods=['GET','POST'])
def register():

    if USERNAME_ == 'normal':
        username = auth.authenticate().strip()
    else:
        username = USERNAME_

    event_id = request.args.get('event_id')
    details = get_details(event_id)

    if request.method == 'POST':
        if request.form.get('Accept') != None:
            status = "accepted"
        elif request.form.get('Decline') != None:
            status = "declined"
        elif request.form.get('Undecided') != None:
            status = 'undecided'
        
        print("status: " + str(status))
        update_participant(event_id, username, status)
        return redirect(url_for('index'))

    html = render_template('register.html', event_id = event_id, username = username, details = details)
    response = make_response(html)

    return response


#-----------------------------------------------------------------------

@app.route('/eventdetails', methods=['GET', 'POST'])

def event_details():

    if USERNAME_ == 'normal':
        username = auth.authenticate().strip()
    else:
        username = USERNAME_

    event_id = request.args.get('event_id')
    details = get_details(event_id)

    if request.method == 'POST':
            # update 1 participant if added
        if request.form.get('Accept') != None:
            status = "accepted"
        elif request.form.get('Decline') != None:
            status = "declined"
        elif request.form.get('Undecided') != None:
            status = 'undecided'

        update_participant(event_id, username, status)
        return redirect(url_for('index'))
  
    details = get_details(event_id)
    html = render_template('eventdetails-1.html', details = details, event_id = event_id, username = username)
    response = make_response(html)
    return response

#-----------------------------------------------------------------------

@app.route('/myevents', methods=['GET', 'POST'])

def my_events():
    if USERNAME_ == 'normal':
        username = auth.authenticate().strip()
    else:
        username = USERNAME_


    status = 'not checked'
    if request.method == 'GET':
        print("ITO IF")
        status = request.args.get('status')
        print("GOT GET STATUS")
    if status == None:
        status = 'attending'

    events = None
    if status == 'attending':
        print("GETTING")
        events = get_yes_events(username)
    elif status == 'uncertain':
        events = get_maybe_events(username)
    elif status == 'not_attending':
        events = get_no_events(username)
    else:
        print('NONE OF THE OPTIONS')
    
    print("PAST IF")


    html = render_template('event.html', status=status, username=username, events=events)
    print("BEFORE MAKING RESPONSE")
    response = make_response(html)
    return response

#-----------------------------------------------------------------------
@app.route('/eventupdate', methods=['GET', 'POST'])

def event_update():

    if USERNAME_ == 'normal':
        username = auth.authenticate().strip()
    else:
        username = USERNAME_

    event_id = request.args.get('event_id')
    details = get_details(event_id)

    if request.method == 'POST':
            # update 1 participant if added
        participant_id = request.form.get('participant_id')
        if participant_id != None: 
            invite_participant([event_id, participant_id])

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
    
    details = get_details(event_id)
    html = render_template('eventupdate-1.html', details = details, event_id = event_id, username = username)
    response = make_response(html)
    return response

if __name__ == '__main__':
    app.run(debug=True)

