import string
import imdb
import re
import os
import httplib
import commonSettings
import models.movie as movie

def appendHD(word):
	hd = ''
	if (string.find(word, '720') != -1):
		hd =' [720]'
	elif (string.find(word, '1080') != -1):
		hd = ' [1080]'
	return hd

def appendExtension(word):
	return word[string.rfind(word, '.'):]

def isVideo(fileName):
	result = False
	extension = fileName[string.rfind(fileName, '.'):]
	if extension == '.mkv':
		result = True
	elif extension == '.avi':
		result = True
	elif extension == '.mp4':
		result = True
	elif extension == '.ogm':
		result = True
	return result

def isOfMovieSize(fileName):
	return True
	result = False
	if os.path.getsize(fileName) >= 629145600:
		result = True
	return result

def getSeries(fileName):
	parsed = re.search("([Ss][\d]+[Xx_\.\s]?[Ee][Pp]?[\d]+)|([_\.\s][\d]+[Xx][\d]+[_\.\s])", fileName)
	if parsed == None:
		return None
	series =  fileName[:parsed.start(0)]
	for c in string.punctuation:
		series = series.replace(c, ' ')
	series = series.lower()
	series = string.capwords(series)
	
	parsedNumbers = re.findall("\d+", parsed.group(0))
	season = parsedNumbers[0]
	if len(season) == 1:
		season = '0'+season
	episode = parsedNumbers[1]
	if len(episode) ==1:
		episode = '0'+episode

	return [series, season, episode]

def filter(word):
	word = word.lower()
	word = string.replace(word, 'demonoid.me', '')
	word = string.replace(word, 'avchd', '')
	word = string.replace(word, '++demonoid.me++', '')
	return word

def findTitles(fileName):
	a = imdb.IMDb()
	filteredFileName = filter(fileName)
	fileNameArray = re.findall(r'[^\s_.\[\]\(\)-]+', filteredFileName)
	i = 0
	titles = []
	movies = []
	while True:
		results = a.search_movie(string.replace(','.join(fileNameArray[0:i+1]), ',', ' '))
		if len(results) != 0 and i!= len(fileNameArray):
			#print "Result set for ",string.replace(','.join(testArray[0:i+1]), ',', ' ')," is of size:",len(results)
			#print 4*' ',results[0]['long imdb canonical title']
			newMovie = movie.createAsPending(results[0]['title'])
			newMovie.year = results[0]['year']
			print "Found ", newMovie.title
			try:
				titles.index(newMovie.title)
			except ValueError:
				titles.append(newMovie.title)
				movies.append(newMovie)
			i=i+1
		else:
			break
	#print '\n','Final result for ',string.replace(','.join(testArray[0:i]), ',', ' '),' is of size:',len(results),'\n'
	return movies

def findTitlesRaw(fileName):
	a = imdb.IMDb()
	filteredFileName = filter(fileName)
	results = a.search_movie(filteredFileName)
	titles = []
	for i in range(0, 5):
		if i >= len(results):
			break
		titles.append('%s (%s)' % (results[i]['title'], results[i]['year']))
	return titles

def sendXbmcNotification(title, message):
	title = string.replace(title, ' ', '%20')
	message = string.replace(message, ' ', '%20')
	try:
		settings = commonSettings.systemSettings()
		conn = httplib.HTTPConnection('localhost', settings.xbmcPort, timeout=1)
		conn.connect()
		conn.request('GET', '/xbmcCmds/xbmcHttp?command=ExecBuiltIn(Notification('+title+','+message+'))')
		r = conn.getresponse()
		conn.close()
	except:
		print "Had a problem sending message to XBMC"
