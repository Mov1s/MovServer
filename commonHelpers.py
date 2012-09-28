import string, imdb, re, os, httplib

import models.movie as movie
import models.series as series
import helpers.titleHandler as titleHandler
import helpers.settingsManager as settingsManager

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

def findImdbSeriesLikeTitle(fileName):
	imdbContext = imdb.IMDb()
	fileNameArray = titleHandler.returnWellFormatedArrayFromTitle(fileName)

	seriesTitles = {}
	serieses = []
	lastSuccessfulSeries = ''
	for i in range(0, len(fileNameArray)):		
		partialFileName = titleStringFromIndexOfTitleArray(fileNameArray, i)
		imdbResults = imdbContext.search_movie(partialFileName)

		loop = 3 if len(imdbResults) >= 3 else len(imdbResults)
		for j in range(0, loop):
			imdbResult = imdbResults[j]
			if imdbResult['kind'] == 'tv series':
				newSeries = series.create(imdbResult['title'])
				if not newSeries.title in seriesTitles:
					seriesTitles[newSeries.title] = True
					serieses.append(newSeries)
				lastSuccessfulSeries = partialFileName
	serieses = titleHandler.orderTvArrayByMatchingSeries(serieses, lastSuccessfulSeries)
	return serieses

def findImdbMoviesLikeTitle(fileName):
	imdbContext = imdb.IMDb()
	fileNameArray = titleHandler.returnWellFormatedArrayFromTitle(fileName)

	titles = {}
	movies = []
	lastSuccessfulTitle = ''
	for i in range(0, len(fileNameArray)):
		partialFileName = titleStringFromIndexOfTitleArray(fileNameArray, i)
		imdbResults = imdbContext.search_movie(partialFileName)

		loop = 3 if len(imdbResults) >= 3 else len(imdbResults)
		for j in range(0, loop):
			imdbResult = imdbResults[j]
			newMovie = movie.create(imdbResult['title'])
			if imdbResult.has_key('year'):
				newMovie.year = imdbResult['year']
			try:
				titleIndex = '{0} {1}'.format(newMovie.title, newMovie.year)
				if not titleIndex in titles:
					titles[titleIndex] = True
					movies.append(newMovie)
			except UnicodeEncodeError:
				print "UnicodeEncodeError"
				continue
			lastSuccessfulTitle = partialFileName
	movies = titleHandler.orderMovieArrayByMatchingTitle(movies, lastSuccessfulTitle)
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
		settings = settingsManager.systemSettings()
		conn = httplib.HTTPConnection('localhost', settings.xbmcPort, timeout=1)
		conn.connect()
		conn.request('GET', '/xbmcCmds/xbmcHttp?command=ExecBuiltIn(Notification('+title+','+message+'))')
		r = conn.getresponse()
		conn.close()
	except:
		print "Had a problem sending message to XBMC"

def titleStringFromIndexOfTitleArray(titleArray, index):
	return string.replace(','.join(titleArray[0:index+1]), ',', ' ')