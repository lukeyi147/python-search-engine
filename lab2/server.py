from bottle import route, run, template, request, abort
from operator import itemgetter
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from beaker.middleware import SessionMiddleware
import bottle
import httplib2

# contains {user_email:[history]} dict
hist = {}

# init beaker file based session
session_opts = {
    'session.type': 'file',
    'session.data_dir': './session/',
    'session.auto': True,
}

app = SessionMiddleware(bottle.app(), session_opts)
     
@route('/', method='GET')
def engine():
    # global hist
    global hist

    # get session
    session = bottle.request.environ['beaker.session']

    # check if user signed in and get user_email if signed in
    signed = 'user_email' in session
    if signed:
        user_email = session['user_email']

    # handle sign_in
    if request.GET.get('sign_in',''):
        # flow step1
        flow = flow_from_clientsecrets("client_secret_654777846488-i5oehn8o4rf262ge2afqjebk81hhd45h.apps.googleusercontent.com.json",
            scope='https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email',
            redirect_uri="http://ec2-54-164-28-20.compute-1.amazonaws.com/redirect")
        uri = flow.step1_get_authorize_url()
        bottle.redirect(str(uri))
        
    # handle sign_out
    if request.GET.get('sign_out',''):
        session.delete()
        bottle.redirect("http://ec2-54-164-28-20.compute-1.amazonaws.com")
        
    # handle submit
    if request.GET.get('submit',''):
 
        # result dictionary contains (word, count) info of current keywords entered by user
        results = {}

        # get keywords from user and split by whitespace into keywords list
        keywords = request.query['keywords'].split(" ")

        #############################
        # iterate over keywords entered by user
        for keyword in keywords:

            # ignore whitespace keywords
            if keyword != "":

                # insert keyword into current results, else increment value
                if not keyword in results:
                    results[keyword] = 1
                else:
                    results[keyword] += 1

        ##################
        
        if signed == 1:
            if user_email not in hist:    #if user not in dictionary
                hist.update({user_email:[]})

            # add to end of list
            for keyword in keywords:
                if keyword != "":
                    hist[user_email].append(keyword)

            # truncate list to only 10 most recent elemnts
            hist[user_email] = hist[user_email][-10:]

            # history shows most recent first
            history = list(hist[user_email])
            history.reverse()

            return template('index', results = results, history = history, sgn = signed, u_email = user_email)
        else:
            return template('index', results = results, history = 0, sgn = signed, u_email = 0)

    else:
        # user didn't submit keywords, display empty results
        results = {}        
        if signed == 1:
            if user_email not in hist:    #if user not in dictionary
                hist.update({user_email:[]})

            # history shows most recent first
            history = list(hist[user_email])
            history.reverse()

            return template('index', results = results, history = history, sgn = signed, u_email = user_email)
        else: 
            return template('index', results = results, history = 0, sgn = signed, u_email = 0)
        
@route('/redirect', method='GET')
def redirect_page():
    # get session
    session = bottle.request.environ['beaker.session']

    # flow step2
    code = request.query.get('code', '')
    flow = flow_from_clientsecrets("client_secret_654777846488-i5oehn8o4rf262ge2afqjebk81hhd45h.apps.googleusercontent.com.json",
        scope='https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email',
        redirect_uri="http://ec2-54-164-28-20.compute-1.amazonaws.com/redirect")
    credentials = flow.step2_exchange(code)
    token = credentials.id_token['sub']

    http = httplib2.Http()
    http = credentials.authorize(http)
    
    # get user email and store in session
    users_service = build('oauth2', 'v2', http=http)
    user_document = users_service.userinfo().get().execute()
    session['user_email'] = user_document['email']
    session.save()

    bottle.redirect("http://ec2-54-164-28-20.compute-1.amazonaws.com")
    
    
run(app = app, host='0.0.0.0', port=80, debug=True)


