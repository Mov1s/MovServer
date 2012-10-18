import re, string

#String level formating functions -----------------------------------------------
#--------------------------------------------------------------------------------
def removePunctuation(title):
	title = re.sub('[%s]' % re.escape(string.punctuation), ' ', title)
	return title

def normalizeCase(title):
	return title.lower()

def replaceAbbreviations(title):
	return title

def removeBlacklistedWords(title):
	title = title.replace('demonoid.me', '')
	title = title.replace('avchd', '')
	title = title.replace('++demonoid.me++', '')
	return title

def returnWellFormatedArrayFromTitle(title):
	title = normalizeCase(title)
	title = removeBlacklistedWords(title)
	title = removePunctuation(title)
	title = replaceAbbreviations(title)
	return title.split()

#Array level formating functions ------------------------------------------------
#--------------------------------------------------------------------------------
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

#Name ordering functions --------------------------------------------------------
#--------------------------------------------------------------------------------
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

#Ranking algorithm functions ----------------------------------------------------
#--------------------------------------------------------------------------------
#Needs some work
def resolveTies(movieArray):
	for i in range(0, len(movieArray)):
		if i+1 < len(movieArray):
			thisMovie = movieArray[i]
			nextMovie = movieArray[i+1]
			if thisMovie.title == nextMovie.title:
				tiedMovies.append(thisMovie)

def percentageOfTitleMatch(firstTitle, secondTitle):
	#Format the titles for comparison
	firstArray = returnWellFormatedArrayFromTitle(firstTitle)
	secondArray = returnWellFormatedArrayFromTitle(secondTitle)

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