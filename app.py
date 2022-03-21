

#-----------------------------------------------------------------------
# app.py
#-----------------------------------------------------------------------

from time import localtime, asctime, strftime
from flask import Flask, request, make_response, redirect, url_for
from flask import render_template
from database import search_event, create_event

#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='.')

#-----------------------------------------------------------------------

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        initializer_array = [request.form.get('sport_c'), 
                            request.form.get('location_c'), 
                            request.form.get('date_c'),
                            request.form.get('start_time_c'),
                            request.form.get('end_time_c'),
                            request.form.get('visibility_c'),
                            request.form.get('organizer_id_c')]

        print("INITARRAY")
        print(initializer_array)
        event = create_event(initializer_array)
        query_data = [None, None, None, None, None, None, None]


    if request.method == 'GET':
        query_data = [request.args.get('sport_f'), 
                    request.args.get('location_f'), 
                    request.args.get('date_f'),
                    request.args.get('start_time_f'),
                    request.args.get('end_time_f'),
                    request.args.get('visibility_f'),
                    request.args.get('organizer_id_f')]
        print("QUERYDATA")
        print(query_data)


    print("Arrived before search")
    events = search_event(query_data)
    print("Completed search")
    html = render_template('index.html', 
    events = events)
    response = make_response(html)
    
    return response

#-----------------------------------------------------------------------

@app.route('/profile', methods=['GET'])
def reg_details():
    html = render_template('profile.html')
    response = make_response(html)
    return response



# @app.route('/searchform', methods=['GET'])
# def search_form():

#     error_msg = request.args.get('error_msg')
#     if error_msg is None:
#         error_msg = ''

#     prev_author = request.cookies.get('prev_author')
#     if prev_author is None:
#         prev_author = '(None)'

#     html = render_template('searchform.html',
#         ampm=get_ampm(),
#         current_time=get_current_time(),
#         error_msg=error_msg,
#         prev_author=prev_author)
#     response = make_response(html)
#     return response

# #-----------------------------------------------------------------------

# @app.route('/searchresults', methods=['GET'])
# def search_results():

#     author = request.args.get('author')
#     if (author is None) or (author.strip() == ''):
#         error_msg = 'Please type an author name.'
#         return redirect(url_for('search_form', error_msg=error_msg))

#     books = search(author)  # Exception handling omitted

#     html = render_template('searchresults.html',
#         ampm=get_ampm(),
#         current_time=get_current_time(),
#         author=author,
#         books=books)
#     response = make_response(html)
#     response.set_cookie('prev_author', author)
#     return response
