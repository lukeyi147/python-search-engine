from bottle import route, run, template, request, abort
from operator import itemgetter
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
import bottle
import httplib2

#History dictionary contains (word, count) pairs for all words entered in field
hist = {}

#Flag for indicating signed in status
signed = 0

#The email of the signed in user
user_email = None
                                
@route('/', method='GET')

def engine():
    global signed
    global user_email
    if request.GET.get('sign_in',''):
        signed = 1
        flow = flow_from_clientsecrets("client_secret_864736965004-d6snoqp3e8d97nh17c9b7pgisaqhjff2.apps.googleusercontent.com.json",
            scope='https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email',
            redirect_uri="http://localhost:8080/redirect")
        uri = flow.step1_get_authorize_url()
        bottle.redirect(str(uri))
        
        
    if request.GET.get('sign_out',''):
        signed = 0
        bottle.redirect("http://localhost:8080")
        
    if request.GET.get('submit',''):
    #User has submitted keywords

        global hist

        #Result dictionary contains (word, count) info of current keywords entered by user
        results = {}

        #Get keywords from user and split by whitespace into keywords list
        keywords = request.query['keywords'].split(" ")
        #############################
        #Iterate over keywords entered by user
        for keyword in keywords:

            #Ignore whitespace keywords
            if keyword != "":

                #Insert keyword into current results, else increment value
                if not keyword in results:
                    results[keyword] = 1
                else:
                    results[keyword] += 1

        ##################
        if signed == 1:
            if user_email not in hist:    #if user not in dictionary
                hist.update({user_email:[]})
            print keywords
            hist[user_email] = hist[user_email] + keywords
            hist[user_email] = hist[user_email][-11:-1]

               
                #add keywords to end of list, then truncate before updating list in dictionary
                
        if signed == 1 :return template('index', results = results, history = hist[user_email], sgn = signed, u_email = user_email)
        if signed == 0 :return template('index', results = results, history = 0, sgn = signed, u_email = user_email)

    else:
    #User didn't submit keywords, display empty results, and display top 20 history

        results = {}
        #sorted_history = sorted(history.iteritems(), key=itemgetter(1), reverse=True)
        
        if signed == 1 :
            if user_email not in hist:    #if user not in dictionary
                hist.update({user_email:[]})
            return template('index', results = results, history = hist[user_email], sgn = signed, u_email = user_email)
        if signed == 0 :return template('index', results = results, history = 0, sgn = signed, u_email = user_email)
        
@route('/redirect', method='GET')
def redirect_page():
    global user_email    
    code = request.query.get('code', '')
    flow = flow_from_clientsecrets("client_secret_864736965004-d6snoqp3e8d97nh17c9b7pgisaqhjff2.apps.googleusercontent.com.json",
        scope='https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email',
        redirect_uri="http://localhost:8080/redirect")
    credentials = flow.step2_exchange(code)
    token = credentials.id_token['sub']

    http = httplib2.Http()
    http = credentials.authorize(http)
    
    #Get user email
    users_service = build('oauth2', 'v2', http=http)
    user_document = users_service.userinfo().get().execute()
    user_email = user_document['email']    
    bottle.redirect("http://localhost:8080")
    
    
run(host='localhost', port=8080, debug=True)


