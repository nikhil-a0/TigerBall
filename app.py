#-----------------------------------------------------------------------
# app.py
#-----------------------------------------------------------------------

from time import localtime, asctime, strftime
from flask import Flask, request, make_response, redirect, url_for
from flask import render_template
from keys import APP_SECRET_KEY
from db import search_event, create_event, get_details, invite_participant,\
    update_event, search_pending_event, update_participant, delete_old_events,\
    get_status_events, create_group, view_groups, get_group_details,\
    add_to_group, leave_group
from config import USERNAME_, ENVIRONMENT_, DATABASE_URL
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from python_http_client.exceptions import HTTPError
import json
from sys import stderr
from req_lib import getOneUndergrad


#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='templates')

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = APP_SECRET_KEY


import auth

toOpen = 0

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

    delete_old_events()
    pending_events = search_pending_event(username)
    query_data = ['','','','','','','']

    if request.method == 'GET':
        query_data = [request.args.get('sport'),
                    request.args.get('skill_level'),
                    request.args.get('capacity'),
                    request.args.get('date'),
                    request.args.get('start_time'),
                    request.args.get('end_time')]
        for i in range(0, len(query_data)):
            if query_data[i] is None:
                query_data[i] = ''
    
#  
    # print("after get")
    # print(pending_events)
    events = search_event(query_data)
    global toOpen
    html = render_template('pend-3.html', events = events, username = username, pending_events = pending_events, updatedEventValue = toOpen) 
    toOpen = 0
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

#-----------------------------------------------------------------------

@app.route('/profile', methods=['GET', 'POST'])

def profile():
    if USERNAME_ == 'normal':
        username = auth.authenticate().strip()
    else:
        username = USERNAME_

    groups = view_groups(username)

    html = render_template('profile.html', username=username, groups=groups)
    response = make_response(html)
    return response

#-----------------------------------------------------------------------

@app.route('/creategroup', methods=['GET','POST'])
def creategroup():
    if USERNAME_ == 'normal':
        username = auth.authenticate().strip()
    else:
        username = USERNAME_

    if request.method == 'POST':
        # members are space-separated netids
        members = request.form.get('members')
        groupname = request.form.get('groupname')
        memlist = members.split(' ')
        initializer_array = [groupname] + memlist
        create_group(initializer_array, username)
        return redirect(url_for('profile'))

    html = render_template('creategroup.html', username=username)
    response = make_response(html)

    return response

#-----------------------------------------------------------------------

@app.route('/groupdetails', methods=['GET', 'POST'])
def group_details():
    if USERNAME_ == 'normal':
        username = auth.authenticate().strip()
    else:
        username = USERNAME_

    group_id = request.args.get('group_id')
    
    # [groupname, member, member, ...]
    groupdets = get_group_details(group_id)

    if request.method == 'POST':
        # space-separated netids
        newmems = request.form.get('newmems')
        netids = newmems.split(' ')
        add_to_group(group_id, netids)
        return redirect(url_for('groupdetails'))

    html = render_template('groupdetails.html', username=username, groupdets=groupdets, group_id=group_id)
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
        print("GOT into POST method from Accept")

        if details[0].get_organizer() != username:
                # update 1 participant if added
            if request.form.get('Accept') != None:
                status = "accepted"
            elif request.form.get('Decline') != None:
                status = "declined"
            elif request.form.get('Undecided') != None:
                status = 'undecided'

            update_participant(event_id, username, status)

            global toOpen
            toOpen = event_id
            return redirect(url_for('index'))
            

        else:
            print("IN POST REQUEST")
            netid = request.form.get('net_id')
            print("netid: " + netid)
                # update 1 participant if added
            # participant_id = request.form.get('participant_id')
            # validate netid
            if netid != None:
                try:
                    req = getOneUndergrad(netid=netid)
                    if req.ok:  
                        undergrad = req.json()
                        # add the participant to the eventsparticipants table
                        invite_participant([event_id, undergrad['net_id']])

                        # send email notification of invitation
                            
                        details = get_details(event_id)[0]

                        organizer_req = getOneUndergrad(netid=details.get_organizer())
                        organizer = organizer_req.json()
                        print("SHOULD BE NIKHIL:" + undergrad['first_name'])

                        message = Mail(
                            from_email='tigerballprinceton@gmail.com',
                            to_emails=undergrad['email'])
                        message.template_id = 'd-6deb7d2a35654298acc547d6f44665ad'
                        message.dynamic_template_data = {
                            "participant_first_name": undergrad['first_name'],    
                            "organizer_first_name": organizer['first_name'],
                            "sport": details.get_sport(),
                            "date": details.get_date(),
                            "start_time": details.get_starttime(),
                            "end_time": details.get_endtime(),
                            "location": details.get_location()
                        }
                        try:
                            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                            response = sg.send(message)
                            print(response.status_code)
                            print(response.body)
                            print(response.headers)

                        except Exception as ex:
                            print(ex, file=stderr)
                
                except Exception as ex:
                    html = "<div class='px-2'><p> A server error occurred. \
                        Please contact the system administrator. </p></div>"
                    print(ex, file=stderr)


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
    

    if details[0].get_organizer() != username:
        html = render_template('eventdetails-1.html', details = details, event_id = event_id, username = username)
    else:
        html = render_template('eventupdate-2.html', details = details, event_id = event_id, username = username)
    
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
        status = request.args.get('status')
    if status == None:
        status = 'attending'

    events = get_status_events(username, status)
    
    html = render_template('event2.html', status=status, username=username, events=events)
    response = make_response(html)
    return response

@app.route('/get_my_events', methods=['GET'])



def get_my_events():
    if USERNAME_ == 'normal':
        username = auth.authenticate().strip()
    else:
        username = USERNAME_
        
    status = 'not checked'
    if request.method == 'GET':
        status = request.args.get('status')
    if status == None:
        status = 'attending'

    events = get_status_events(username, status)
    html = render_template('my_events.html', status=status, username=username, events=events)
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
        print("IN POST REQUEST")
        netid = request.form.get('net_id')
        print("netid: " + netid)
            # update 1 participant if added
        # participant_id = request.form.get('participant_id')
        # validate netid
        if netid != None:
            try:
                req = getOneUndergrad(netid=netid)
                if req.ok:  
                    undergrad = req.json()
                    # add the participant to the eventsparticipants table
                    invite_participant([event_id, undergrad['net_id']])

                    # send email notification of invitation
                        
                    details = get_details(event_id)[0]

                    organizer_req = getOneUndergrad(netid=details.get_organizer())
                    organizer = organizer_req.json()
                    print("SHOULD BE NIKHIL:" + undergrad['first_name'])

                    message = Mail(
                        from_email='tigerballprinceton@gmail.com',
                        to_emails=undergrad['email'])
                    message.template_id = 'd-6deb7d2a35654298acc547d6f44665ad'
                    message.dynamic_template_data = {
                        "participant_first_name": undergrad['first_name'],    
                        "organizer_first_name": organizer['first_name'],
                        "sport": details.get_sport(),
                        "date": details.get_date(),
                        "start_time": details.get_starttime(),
                        "end_time": details.get_endtime(),
                        "location": details.get_location()
                    }
                    try:
                        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                        response = sg.send(message)
                        print(response.status_code)
                        print(response.body)
                        print(response.headers)

                    except Exception as ex:
                        print(ex, file=stderr)
            
            except Exception as ex:
                html = "<div class='px-2'><p> A server error occurred. \
                    Please contact the system administrator. </p></div>"
                print(ex, file=stderr)


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

        global toOpen
        toOpen = event_id

    return redirect(url_for('index'))
        
    
    




#-----------------------------------------------------------------------
@app.route('/participant', methods=['GET', 'POST'])

def participant():

    event_id = request.args.get('event_id')
    print("EVENT ID:" + event_id)
    participantID = request.args.get('participant_id')
    print("PARTICIPANT ID: " + participantID)

    html = '<table class="table table-striped">\
                        <tbody id="resultsRows">\
                        <tr><th>Invite the following student:</th></tr>'

    if len(str(participantID)) >= 3:

        # Display clickable button to invite the specified student 
        try:

            req = getOneUndergrad(netid=participantID)
            if req.ok:  
                undergrad = req.json()
                pattern=pattern='<tr><td><form action="/eventupdate?event_id=%s" method="post" name="invitevalidatedparticipant"><button name="net_id" value=%s>%s %s</button></form></td></tr>'
                html += pattern % (event_id, undergrad['net_id'], undergrad['full_name'], undergrad['class_year'])
            
            else:
                html += '<tr><td> Not a valid netid </td></tr>'

            html += "</tbody></table>"
            response = make_response(html)

        except Exception as ex:
            html = "<div class='px-2'><p> A server error occurred. \
                Please contact the system administrator. </p></div>"
            print(ex, file=stderr)

            response = make_response(html)
        
        return response
    
    else:
        html='<table class="table table-striped">\
                        <tbody id="resultsRows">\
                        <tr><th>Netid must be at least three characters. </th></tr>'
        

if __name__ == '__main__':
    app.run(debug=True)

