from bottle import route, run, template, request
from operator import itemgetter

#History dictionary contains (word, count) pairs for all words entered in field
history = {}

@route('/', method='GET')
def engine():
	if request.GET.get('submit',''):
		#User has submitted keywords

		global history

		#Result dictionary contains (word, count) info of current keywords entered by user
		results = {}

		#Get keywords from user and split by whitespace into keywords list
		keywords = request.query['keywords'].split(" ")

		#Iterate over keywords entered by user
		for keyword in keywords:

			#Ignore whitespace keywords
			if keyword != "":

				#Insert keyword into history, else increment value
				if not keyword in history:
					history[keyword] = 1
				else:
					history[keyword] += 1

				#Insert keyword into current results, else increment value
				if not keyword in results:
					results[keyword] = 1
				else:
					results[keyword] += 1

		#Sort history and display top 20 history items only
		sorted_history = sorted(history.iteritems(), key=itemgetter(1), reverse=True)
		return template('index', results = results, history = sorted_history[:20])

	else:
		#User didn't submit keywords, display empty results, and display top 20 history

		results = {}
		sorted_history = sorted(history.iteritems(), key=itemgetter(1), reverse=True)
		return template('index', results = results, history = sorted_history[:20])

run(host='127.0.0.1', port=8080, debug=True)