

#-----------------------------------------------------------------------
# app.py
#-----------------------------------------------------------------------

from time import localtime, asctime, strftime
from flask import Flask, request, make_response, redirect, url_for
from flask import render_template
from database import search_event, create_event

#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='templates')

#-----------------------------------------------------------------------

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method.get == 'POST':
        initializer_array = [request.args.get('sport_c'), 
                            request.args.get('location_c'), 
                            request.args.get('date_c'),
                            request.args.get('start_time_c'),
                            request.args.get('end_time_c'),
                            request.args.get('visibility_c'),
                            request.args.get('organizer_id_c')]

        create_event(initializer_array)




    if request.method.get == 'GET':
        query_data = [request.args.get('Sport'), 
                            request.args.get('Location'), 
                            request.args.get('Datetime')]

        events = search_event(query_data)[1]
        print(events) 
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
