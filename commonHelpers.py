import string, imdb, tvdb_api, re, httplib

import models.movie as movie
import models.series as series
import helpers.titleHandler as titleHandler
import helpers.settingsManager as settingsManager

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
	tvdbContext = tvdb_api.Tvdb()
	fileNameArray = titleHandler.returnWellFormatedArrayFromTitle(fileName)

	seriesTitles = {}
	serieses = []
	lastSuccessfulSeries = ''
	for i in range(0, len(fileNameArray)):	
		partialFileName = titleStringFromIndexOfTitleArray(fileNameArray, i)
		try:
			print partialFileName
			tvdbResult = tvdbContext[partialFileName]
			print tvdbResult
			newSeries = series.create(tvdbResult['seriesname'])
			if not newSeries.title in seriesTitles:
				seriesTitles[newSeries.title] = True
				serieses.append(newSeries)
				lastSuccessfulSeries = partialFileName
		except:
			continue
				
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

		loop = 15 if len(imdbResults) >= 15 else len(imdbResults)
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

def sendXbmcLibraryUpdate():
	try:
		settings = settingsManager.systemSettings()
		conn = httplib.HTTPConnection('localhost', settings.xbmcPort, timeout=1)
		conn.connect()
		conn.request('GET', '/xbmcCmds/xbmcHttp?command=ExecBuiltIn(UpdateLibrary(video))')
		r = conn.getresponse()
		conn.close()
	except:
		print "Had a problem updating XBMC's library"

def titleStringFromIndexOfTitleArray(titleArray, index):
	return string.replace(','.join(titleArray[0:index+1]), ',', ' ')