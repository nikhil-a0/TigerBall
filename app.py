#-----------------------------------------------------------------------
# app.py
#-----------------------------------------------------------------------
from time import localtime, asctime, strftime
from flask import Flask, request, make_response, redirect, url_for
from flask import render_template
# from keys import APP_SECRET_KEY
from db import search_event, create_event, get_details, invite_participant,\
    update_event, search_pending_event, update_participant, delete_old_events,\
    get_status_events, create_group, view_groups, get_group_details, delete_todays_old_events,\
    add_to_group, leave_group, invite_group, find_group_id
from datetime import date, datetime, time
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from python_http_client.exceptions import HTTPError
import json
from sys import stderr
from req_lib import getOneUndergrad


#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='templates')

DATABASE_URL = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = os.environ.get('APP_SECRET_KEY')
USERNAME_ = os.environ.get('USERNAME_')

import auth

toOpen = 0
USERNAME_ADMIN = ''


#-----------------------------------------------------------------------
# Landing page
@app.route('/', methods=['GET', 'POST'])
def landing():
    error_message = ''

    if request.method == 'POST':
        test_username = request.form.get('username')
        test_password = request.form.get('password')

        
        if test_password == 'cos333grader':
            global USERNAME_ADMIN
            USERNAME_ADMIN = str(test_username) 
            return redirect(url_for('homepage'))
        else:
            error_message = 'Sorry, only graders have access to this function.'

    html = render_template('landingpage.html', error_message = error_message)
    response = make_response(html)
    return response

#-----------------------------------------------------------------------
# Main page
@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    global USERNAME_ADMIN
    if USERNAME_ADMIN != '':
        username = USERNAME_ADMIN
    elif os.environ.get('USERNAME_') == 'normal':
        username = auth.authenticate().strip()
        


    # Pending Events

    delete_old_events()
    delete_todays_old_events()
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
            if query_data[i] is None or query_data[0] == 'none':
                query_data[i] = ''
    
#  
    # print("after get")
    # print(pending_events)
    try:
        events = search_event(query_data)
    except Exception as ex:
        print(ex, file='stderr')
        events = []
    
    global toOpen
    html = render_template('pend-3.html', events = events, username = username,
    pending_events = pending_events, updatedEventValue = toOpen, date = date.today(), time = datetime.now().time().strftime("%I:%M %p")) 
    toOpen = 0
    response = make_response(html)
    
    return response

#-----------------------------------------------------------------------
# Create Event Form data (#create) is submitted to here
@app.route('/create', methods=['GET','POST'])
def create():

    global USERNAME_ADMIN
    if USERNAME_ADMIN != '':
        username = USERNAME_ADMIN
    elif os.environ.get('USERNAME_') == 'normal':
        username = auth.authenticate().strip()


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

#-----------------------------------------------------------------------
# Shows groups
@app.route('/profile', methods=['GET', 'POST'])

def profile():
    global USERNAME_ADMIN
    if USERNAME_ADMIN != '':
        username = USERNAME_ADMIN
    elif os.environ.get('USERNAME_') == 'normal':
        username = auth.authenticate().strip()

    groups = view_groups(username)

    html = render_template('profile.html', username=username, groups=groups)
    response = make_response(html)
    return response

#-----------------------------------------------------------------------

@app.route('/creategroup', methods=['GET','POST'])
def creategroup():
    global USERNAME_ADMIN
    if USERNAME_ADMIN != '':
        username = USERNAME_ADMIN
    elif os.environ.get('USERNAME_') == 'normal':
        username = auth.authenticate().strip()

    if request.method == 'POST':
        # members are space-separated netids
        members = request.form.get('members')
        groupname = request.form.get('groupname')
        print(members)
        print(groupname)
        memlist = members.split(' ')
        initializer_array = [groupname] + memlist
        create_group(initializer_array, username)
        return redirect(url_for('profile'))

    html = render_template('creategroup.html', username=username)
    response = make_response(html)

    return response

#-----------------------------------------------------------------------

@app.route('/groupdetails', methods=['GET', 'POST'])
def groupdetails():
    global USERNAME_ADMIN
    if USERNAME_ADMIN != '':
        username = USERNAME_ADMIN
    elif os.environ.get('USERNAME_') == 'normal':
        username = auth.authenticate().strip()

    group_id = request.args.get('group_id')
    
    # [groupname, member, member, ...]
    groupdets = get_group_details(group_id)

    if request.method == 'POST':
        netid = request.form.get('net_id')
        if netid is not None:
            add_to_group(group_id, [netid])
        return redirect(url_for('profile'))
        #return redirect('groupdetails?group_id='+group_id)

    html = render_template('groupdetails.html', username=username, groupdets=groupdets, group_id=group_id)
    response = make_response(html)

    return response

@app.route('/leavegroup', methods=['GET', 'POST'])
def leavegroup():
    global USERNAME_ADMIN
    if USERNAME_ADMIN != '':
        username = USERNAME_ADMIN
    elif os.environ.get('USERNAME_') == 'normal':
        username = auth.authenticate().strip()

    group_id = request.args.get('group_id')
    
    leave_group(group_id, username)

    return redirect(url_for('profile'))

#-----------------------------------------------------------------------

@app.route('/eventdetails', methods=['GET', 'POST'])

def event_details():
    global USERNAME_ADMIN
    if USERNAME_ADMIN != '':
        username = USERNAME_ADMIN
    elif os.environ.get('USERNAME_') == 'normal':
        username = auth.authenticate().strip()

    event_id = request.args.get('event_id')
    details = get_details(event_id)

    if request.method == 'POST':

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
            return redirect(url_for('homepage'))
            

    if details[0].get_organizer() != username:
        html = render_template('eventdetails-1.html', details = details, event_id = event_id, username = username)
    else:
        html = render_template('eventupdate-2.html', details = details, event_id = event_id, username = username)
    
    response = make_response(html)
    return response


#-----------------------------------------------------------------------

@app.route('/myevents', methods=['GET', 'POST'])
def my_events():
    global USERNAME_ADMIN
    if USERNAME_ADMIN != '':
        username = USERNAME_ADMIN
    elif os.environ.get('USERNAME_') == 'normal':
        username = auth.authenticate().strip()


    status = 'not checked'
    if request.method == 'GET':
        status = request.args.get('status')
    if status == None:
        status = 'attending'

    events = get_status_events(username, status)
    # for event in events:
    #     print(event.get_sport())
    #     print(event.get_date())
    #     print(event.get_starttime())
    #     print(event.get_endtime())
    #     print('NEXT')

    
    html = render_template('event2.html', status=status, username=username, events=events, date = date.today(), time = datetime.now().time().strftime("%I:%M %p"))
    response = make_response(html)
    return response

#-----------------------------------------------------------------------
@app.route('/get_my_events', methods=['GET'])
def get_my_events():
    global USERNAME_ADMIN
    if USERNAME_ADMIN != '':
        username = USERNAME_ADMIN
    elif os.environ.get('USERNAME_') == 'normal':
        username = auth.authenticate().strip()

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
    global USERNAME_ADMIN
    if USERNAME_ADMIN != '':
        username = USERNAME_ADMIN
    elif os.environ.get('USERNAME_') == 'normal':
        username = auth.authenticate().strip()

    event_id = request.args.get('event_id')
    details = get_details(event_id)

    if request.method == 'POST':
        netid = request.form.get('net_id')

        # update 1 participant if added
        # validate netid
        if netid != None:

            try:
                req = getOneUndergrad(netid=netid)
                if req.ok:  
                    undergrad = req.json()
                    # add the participant to the eventsparticipants table
                    if invite_participant([event_id, undergrad['net_id']]):
                    # send email notification of invitation
                        details = get_details(event_id)[0]

                        organizer_req = getOneUndergrad(netid=details.get_organizer())
                        if organizer_req.ok:
                            organizer = organizer_req.json()

                            message = Mail(
                                from_email='tigerballprinceton@gmail.com',
                                to_emails=undergrad['email'])
                            message.template_id = 'd-6deb7d2a35654298acc547d6f44665ad'
                            message.dynamic_template_data = {
                                "participant_first_name": undergrad['first_name'],    
                                "organizer_first_name": organizer['first_name'],
                                "sport": details.get_sport(),
                                "date": str(details.get_date().strftime('%-m/%-d')),
                                "start_time": str(details.get_starttime().strftime('%I:%M %p')),
                                "end_time": str(details.get_endtime().strftime('%I:%M %p')),
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
                print(ex, file=stderr)

        else: 
            initializer_array = [event_id,
                                    request.form.get('sport'), 
                                    request.form.get('location'), 
                                    request.form.get('skill_level'),
                                    request.form.get('date'),
                                    request.form.get('start_time'),
                                    request.form.get('end_time'),
                                    request.form.get('capacity'),
                                    request.form.get('visibility')]
            
            update_event(initializer_array)

        global toOpen
        toOpen = event_id

    return redirect(url_for('homepage'))
        
    
    
#-----------------------------------------------------------------------
@app.route('/eventupdategroup', methods=['GET', 'POST'])

def event_update_group():
    global USERNAME_ADMIN
    if USERNAME_ADMIN != '':
        username = USERNAME_ADMIN
    elif os.environ.get('USERNAME_') == 'normal':
        username = auth.authenticate().strip()

    event_id = request.args.get('event_id')
    details = get_details(event_id)

    if request.method == 'POST':
        print("IN POST REQUEST EVENT UPDATE")
        
        # here netid refers to the group id
        netid = request.form.get('net_id')

            # update 1 participant if added
        # participant_id = request.form.get('participant_id')
        # validate netid
        if netid != None:
            print("NETID DON't WORK !=  None")
            try:
                invite_group(event_id, netid)
            except Exception as ex:
                html = "<div class='px-2'><p> Could not invite group. \
                    Please contact the system administrator. </p></div>"
                print(ex, file=stderr)
        else:
            initializer_array = [event_id,
                                request.form.get('sport_c'), 
                                request.form.get('location_c'), 
                                request.form.get('skill_level_c'),
                                request.form.get('date_c'),
                                request.form.get('start_time_c'),
                                request.form.get('end_time_c'),
                                request.form.get('capacity_c'),
                                request.form.get('visibility_c')]
        
            print(initializer_array)
            
            update_event(initializer_array)

        global toOpen
        toOpen = event_id

    return redirect(url_for('homepage'))



#-----------------------------------------------------------------------
@app.route('/participant', methods=['GET', 'POST'])

def participant():

    event_id = request.args.get('event_id')
    print("EVENT ID:" + event_id)
    participantID = request.args.get('participant_id')
    print("PARTICIPANT ID: " + participantID)

    html = '<table class="table table-striped">\
                        <tbody id="resultsRows">'

    # if len(str(participantID)) >= 3:
    if len(str(participantID)) >= 1:

        # Display clickable button to invite the specified student or group
        try:

            req = getOneUndergrad(netid=participantID)
            if req.ok:  
                html += '<tr><th>Invite the following student:</th></tr>'
                undergrad = req.json()
                pattern=pattern='<tr><td><form action="/eventupdate?event_id=%s" method="post" name="invitevalidatedparticipant"><button name="net_id" value=%s>%s %s</button></form></td></tr>'
                html += pattern % (event_id, undergrad['net_id'], undergrad['full_name'], undergrad['class_year'])
            
            else:
                gid = find_group_id(participantID)
                if gid is not None:
                    html += '<tr><th>Invite the following group:</th></tr>'
                    pattern=pattern='<tr><td><form action="/eventupdategroup?event_id=%s" method="post" name="invitevalidatedparticipant"><button name="net_id" value=%s>%s</button></form></td></tr>'
                    html += pattern % (event_id, gid, participantID)
                else:
                    html += '<tr><th>Invite the following student or group:</th></tr>'
                    html += '<tr><td> Not a valid netid or group name</td></tr>'

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
        response = make_response(html)
        return response

#-----------------------------------------------------------------------
@app.route('/checktiming', methods=['GET'])

def checktiming():
    start_str = request.args.get('start_time')
    end_str = request.args.get('end_time')
    event_str = request.args.get('event_date')

    print("start time str", start_str)
    print("end time str", end_str)
    print("event date", event_str)

    error_message=''

    if start_str and end_str and event_str:
        start_time = datetime.strptime(start_str, '%H:%M').time()
        end_time = datetime.strptime(end_str, '%H:%M').time()
        event_date = datetime.strptime(event_str, '%Y-%m-%d').date()

        print("ENTERED EVENT DATE", event_date)
        print("TODAY's DATE", date.today())

        print("ENTERED ST", start_time)
        print("RIGHT NOW TIME", datetime.now().time())

        error_message = ''

        # Event is today
        if event_date == date.today():
            print("line 481")
            if start_time < datetime.now().time() or end_time < datetime.now().time():
                print("time must be earlier than now")
                error_message = 'error detected, the event cannot start/end in the past'
            if end_time <= start_time:
                error_message = 'error detected, the event\'s end time must be after its start time'
        # Event is not today
        elif end_time <= start_time:
            error_message = 'error detected, the event\'s end time must be after its start time'
        if start_time > time(22, 0, 0) and end_time > time(0, 0, 0) and end_time < time(2, 0, 0):
            error_message = 'no error detected, the event starts before midnight and ends slightly after midnight'
    
    html = "<aside><div><p> "+ error_message + " </p></div></aside>"
    # html = "<div><p>"+ start_time+ " " + end_time + " " + event_date + " </p></div>"
    response = make_response(html)
    return response

#-----------------------------------------------------------------------
@app.route('/addtogroup', methods=['GET'])

def addtogroup():
    group_id = request.args.get('group_id')
    print("group ID:" + group_id)
    participantID = request.args.get('participant_id')
    print("PARTICIPANT ID: " + participantID)

    html = '<table class="table table-striped">\
                        <tbody id="resultsRows">'

    # if len(str(participantID)) >= 3:
    if len(str(participantID)) >= 1:

        # Display clickable button to invite the specified student or group
        try:

            req = getOneUndergrad(netid=participantID)
            if req.ok:  
                html += '<tr><th>Invite the following student to the group:</th></tr>'
                undergrad = req.json()
                pattern=pattern='<tr><td><form action="/groupdetails?group_id=%s" method="post" name="invitevalidatedparticipant"><button name="net_id" value=%s>%s \'%s</button></form></td></tr>'
                html += pattern % (group_id, undergrad['net_id'], undergrad['full_name'], undergrad['class_year'])
            
            else:
                html += '<tr><th>Invite the following student:</th></tr>'
                html += '<tr><td> Not a valid netid or group name</td></tr>'

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
        response = make_response(html)
        return response



    
if __name__ == '__main__':
    app.run(debug=True)

