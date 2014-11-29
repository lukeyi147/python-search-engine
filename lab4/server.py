from bottle import route, run, template, request, abort, error
from operator import itemgetter
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from beaker.middleware import SessionMiddleware
import bottle
import httplib2
import sqlite3 as lite
import ConfigParser

# config parsing
config = ConfigParser.ConfigParser()
config.read("config.conf")
dev = config.getboolean('mode', 'dev')
client_secret = config.get('google_client_secret','client_secret_dev' if dev else 'client_secret_prod')
app_url = config.get('app', 'url_dev' if dev else 'url_prod')
app_url_redirect = app_url + "/redirect"
app_host = config.get('app', 'host_dev' if dev else 'host_prod')
app_port = config.getint('app', 'port_dev' if dev else 'port_prod')
sqlite_db = config.get('db', 'sqlite_db')
page_limit = config.get('search', 'page_limit')

# contains {user_email:[history]} dict
hist = {}

# init beaker file based session
session_opts = {
    'session.type': 'file',
    'session.data_dir': './session/',
    'session.auto': True,
}

app = SessionMiddleware(bottle.app(), session_opts)

@error(404)
def error404(error):
    return template('errorindex')
     
@route('/', method='GET')
def engine():
    # global hist
    global hist

    # db connection
    con = lite.connect(sqlite_db)
    cur = con.cursor()

    # get session
    session = bottle.request.environ['beaker.session']

    # check if user signed in and get user_email if signed in
    signed = 'user_email' in session
    if signed:
        user_email = session['user_email']

    # handle sign_in
    if request.GET.get('sign_in',''):
        # flow step1
        flow = flow_from_clientsecrets(client_secret,
            scope='https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email',
            redirect_uri=app_url_redirect)
        uri = flow.step1_get_authorize_url()
        bottle.redirect(str(uri))
        
    # handle sign_out
    elif request.GET.get('sign_out',''):
        session.delete()
        bottle.redirect(app_url)
        
    # handle submit
    elif request.GET.get('submit',''):
 
        # result dictionary contains (doc_url, page_rank) of docs containing word_id of keyword
        results = []

        # pagination links
        has_prev = False
        has_next = False

        # pagination start offset
        start = request.query.start or '0'
        start = int(start)

        # get keywords from user and split by whitespace into keywords list
        if(request.query.keywords):
            # get only first keyword
            keywords = request.query['keywords'].split(" ")
            keyword = keywords[0]
        else:
            # error if no keyword provided with submit
            return template('errorindex')

        # ignore whitespace keywords
        if keyword != "":
            # query to get word_id
            cur.execute("SELECT word_id FROM lexicon where word = ?", (keyword,))
            result = cur.fetchone()
            if(result):
                # get word_id from keyword
                word_id = result[0]

                # query to get doc_ids that contain word_id
                doc_ids = [ ]
                cur.execute("SELECT doc_id FROM invertedIndex WHERE word_id = ?", (word_id,))
                for row in cur:
                    doc_ids.append(row[0])

                # query to get doc_urls and page_rank of doc_id in doc_ids based on page_limit LIMIT
                # dirty hack to bind start and page_limit to query string
                doc_ids.append(start)
                doc_ids.append(page_limit)
                cur.execute("SELECT doc_url, page_rank FROM documentIndex WHERE doc_id IN (%s) ORDER BY page_rank DESC LIMIT ?, ?" % ("?," * (len(doc_ids)-2))[:-1], doc_ids )
                for row in cur:
                    # add doc_url and page_rank to result list
                    results.append((row[0], row[1]))

                # set has_prev and has_next for pagination
                if int(start) == 0:
                    has_prev = False
                else:
                    has_prev = True
                if len(results) == page_limit:
                    has_next = True
                else:
                    has_next = False
        ##################
        if signed == 1:
            if user_email not in hist:    #if user not in dictionary
                hist.update({user_email:[]})

            # add to end of list
            if keyword != "":
                hist[user_email].append(keyword)

            # truncate list to only 10 most recent elemnts
            hist[user_email] = hist[user_email][-10:]

            # history shows most recent first
            history = list(hist[user_email])
            history.reverse()

            return template('index', results = results, history = history, sgn = signed, u_email = user_email, start = start, page_limit = page_limit, has_next = has_next, has_prev = has_prev)
        else:
            return template('index', results = results, history = 0, sgn = signed, u_email = 0, start = start, page_limit = page_limit, has_next = has_next, has_prev = has_prev)

    elif not request.query:
        # user didn't submit keywords, display empty results
        results = {}        
        if signed == 1:
            if user_email not in hist:    #if user not in dictionary
                hist.update({user_email:[]})

            # history shows most recent first
            history = list(hist[user_email])
            history.reverse()

            return template('index', results = results, history = history, sgn = signed, u_email = user_email, start = 0, page_limit = 0, has_next = 0, has_prev = 0)
        else: 
            return template('index', results = results, history = 0, sgn = signed, u_email = 0, start = 0, page_limit = 0, has_next = 0, has_prev = 0)
        
    else:
        # not recognized query
        return template('errorindex')

@route('/redirect', method='GET')
def redirect_page():
    # get session
    session = bottle.request.environ['beaker.session']

    # flow step2
    code = request.query.get('code', '')
    flow = flow_from_clientsecrets(client_secret,
        scope='https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email',
        redirect_uri=app_url_redirect)
    credentials = flow.step2_exchange(code)
    token = credentials.id_token['sub']

    http = httplib2.Http()
    http = credentials.authorize(http)
    
    # get user email and store in session
    users_service = build('oauth2', 'v2', http=http)
    user_document = users_service.userinfo().get().execute()
    session['user_email'] = user_document['email']
    session.save()

    bottle.redirect(app_url)

run(app = app, host=app_host, port=app_port, debug=True)


