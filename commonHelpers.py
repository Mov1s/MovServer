import string
import imdb
import re
import os
import httplib
import commonSettings
import models.movie as movie
import models.series as series

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
	# return True
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

def findSeries(fileName):
	a = imdb.IMDb()
	fileName = normalizeCase(fileName)
	fileName = removeBlacklistedWords(fileName)
	fileName = removePunctuation(fileName)
	fileNameArray = fileName.split()

	seriesTitles = {}
	serieses = []
	lastSuccessfulSeries = ''
	for i in range(0, len(fileNameArray)):		
		partialFileName = titleStringFromIndexOfTitleArray(fileNameArray, i)
		results = a.search_movie(partialFileName)

		loop = 3 if len(results) >= 3 else len(results)

		for i in range(0, loop):
			r = results[i]
			if r['kind'] == 'tv series':
				newSeries = series.create(r['title'])
				if not newSeries.title in seriesTitles:
					seriesTitles[newSeries.title] = True
					serieses.append(newSeries)
				lastSuccessfulSeries = partialFileName
	serieses = orderTvArrayByMatchingSeries(serieses, lastSuccessfulSeries)
	return serieses

def findMovies(fileName):
	a = imdb.IMDb()
	fileName = normalizeCase(fileName)
	fileName = removeBlacklistedWords(fileName)
	fileName = removePunctuation(fileName)
	fileNameArray = fileName.split()

	i = 0
	titles = {}
	movies = []
	lastSuccessfulTitle = ''
	for i in range(0, len(fileNameArray)):
		partialFileName = titleStringFromIndexOfTitleArray(fileNameArray, i)
		results = a.search_movie(partialFileName)

		loop = 3 if len(results) >= 3 else len(results)

		for i in range(0, loop):
			r = results[i]
			newMovie = movie.create(r['title'])
			if r.has_key('year'):
				newMovie.year = r['year']
			try:
				titleIndex = '{0} {1}'.format(newMovie.title, newMovie.year)
				if not titleIndex in titles:
					titles[titleIndex] = True
					movies.append(newMovie)
			except UnicodeEncodeError:
				print "UnicodeEncodeError"
				continue
			lastSuccessfulTitle = partialFileName
	movies = orderMovieArrayByMatchingTitle(movies, lastSuccessfulTitle)

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

def titleStringFromIndexOfTitleArray(titleArray, index):
	return string.replace(','.join(titleArray[0:index+1]), ',', ' ')

def removePunctuation(title):
	title = re.sub('[%s]' % re.escape(string.punctuation), ' ', title)
	return title

def normalizeCase(title):
	return title.lower()

def replaceNumeralsInArray(titleArray):
	if 'ii' in titleArray:
		titleArray[titleArray.index('ii')] = '2'
	if 'iii' in titleArray:
		titleArray[titleArray.index('iii')] = '3'
	if 'iv' in titleArray:
		titleArray[titleArray.index('iv')] = '4'
	return titleArray

def removeLeadingTheInArray(titleArray):
	if titleArray[0].lower() == 'the':
		del titleArray[0]
	return titleArray

def replaceAbbreviations(title):
	return title

def removeBlacklistedWords(title):
	title = string.replace(title, 'demonoid.me', '')
	title = string.replace(title, 'avchd', '')
	title = string.replace(title, '++demonoid.me++', '')
	return title

def orderMovieArrayByMatchingTitle(movieArray, title):
	sortedMovies = []
	for m in movieArray:
		# titleWithYear = '{0} {1}'.format(m.title, m.year)
		pMatch = percentageOfTitleMatch(m.title, title)
		sortedMovies.append([pMatch, m])
		sortedMovies.sort(reverse=True)
	returnMovies = []
	for m in sortedMovies:
		returnMovies.append(m[1])
	return returnMovies

def orderTvArrayByMatchingSeries(seriesArray, aSeries):
	sortedSeries = []
	for s in seriesArray:
		pMatch = percentageOfTitleMatch(s.title, aSeries)
		sortedSeries.append([pMatch, s])
		sortedSeries.sort(reverse=True)
	returnSeries = []
	for s in sortedSeries:
		returnSeries.append(s[1])
	return returnSeries

#Needs some work
def resolveTies(movieArray):
	for i in range(0, len(movieArray)):
		if i+1 < len(movieArray):
			thisMovie = movieArray[i]
			nextMovie = movieArray[i+1]
			if thisMovie.title == nextMovie.title:
				tiedMovies.append(thisMovie)

def percentageOfTitleMatch(firstTitle, secondTitle):
	#Format the first title for comparison
	firstTitle = normalizeCase(firstTitle)
	firstTitle = removeBlacklistedWords(firstTitle)
	firstTitle = removePunctuation(firstTitle)
	firstTitle = replaceAbbreviations(firstTitle)

	#Format the second title for comparison
	secondTitle = normalizeCase(secondTitle)
	secondTitle = removeBlacklistedWords(secondTitle)
	secondTitle = removePunctuation(secondTitle)
	secondTitle = replaceAbbreviations(secondTitle)

	#Split the formated titles into comparable word arrays
	firstArray = firstTitle.split()
	secondArray = secondTitle.split()

	#Replace numerals
	firstArray = replaceNumeralsInArray(firstArray)
	secondArray = replaceNumeralsInArray(secondArray)

	#Ensure the second array is always the larger of the two
	if len(firstArray) > len(secondArray):
		tempArray = firstArray
		firstArray = secondArray
		secondArray = tempArray

	#Count the matching words between the two titles
	matchingWordCount = 0
	for word in firstArray:
		if word in secondArray:
			matchingWordCount += 1

	# print firstTitle, ' ', secondTitle
	# print '\t({0} / {1})*({2} / {3})'.format(matchingWordCount, len(firstArray), matchingWordCount, len(secondArray))
	percentFirstMatch = float(matchingWordCount) / len(firstArray)
	percentSecondMatch = float(matchingWordCount) / len(secondArray)
	# print '\t', str(percentFirstMatch * percentSecondMatch)
	#Return the percentage of matching words between the two titles
	return percentFirstMatch * percentSecondMatch
