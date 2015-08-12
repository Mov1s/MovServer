import re, string
import helpers.settingsManager as settingsManager

#String level formating functions -----------------------------------------------
#--------------------------------------------------------------------------------
def removePunctuation(title):
  title = re.sub('[%s]' % re.escape(string.punctuation), ' ', title)
  return title

def removeWindowsOffendingPunctuation(title):
  title = title.replace('\'', '')
  title = title.replace(':', '')
  return title

def normalizeCase(title):
  return title.lower()

def replaceAbbreviations(title):
  return title

def removeBlacklistedWords(title):
  options = settingsManager.mediaFileSettings()
  for word in options.blackListedWords:
  	title = title.replace(word, '')
  return title

def returnWellFormatedArrayFromTitle(title):
  title = normalizeCase(title)
  title = removeBlacklistedWords(title)
  title = removeWindowsOffendingPunctuation(title)
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
def orderMovieArrayByMatchingTitle(movieArray, title, originalFileName):
  sortedMovies = []
  for m in movieArray:
    pMatch = percentageOfTitleMatch(m.title, title)
    sortedMovies.append([pMatch, m])
  sortedMovies.sort(reverse=True)
  sortedMovies = resolveTies(sortedMovies, originalFileName)

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

#Debug printing functions -------------------------------------------------------
#--------------------------------------------------------------------------------
def printPercentageArray(percentageMatchedMovieArray, sortedPercentageMatchedMovieArray, reorderedMatchedMovieArray):
  movieFormat = '{0} {1} ({2})'
  for i in range(0, len(percentageMatchedMovieArray)):
    us = percentageMatchedMovieArray[i]
    s = sortedPercentageMatchedMovieArray[i]
    ro = reorderedMatchedMovieArray[i]
    usf = movieFormat.format(round(us[0], 2), us[1].title, us[1].year)
    sf = movieFormat.format(round(s[0], 2), s[1].title, s[1].year)
    rof = movieFormat.format(round(ro[0], 2), ro[1].title, ro[1].year)

    print usf, ' ' * (50 - len(usf)), sf, ' ' * (50 - len(sf)), rof

#Ranking algorithm functions ----------------------------------------------------
#--------------------------------------------------------------------------------
#Breaks ties by promoting movies that are in the right year
def resolveTies(percentageMatchedMovieArray, originalFileName):
  tiedMovies = []
  for i in range(0, len(percentageMatchedMovieArray)):
    if i+1 < len(percentageMatchedMovieArray):
      thisMovie = percentageMatchedMovieArray[i]
      nextMovie = percentageMatchedMovieArray[i+1]
      tiedMovies.append(thisMovie)

      #Break if the next movie has a different match percentage
      if thisMovie[0] != nextMovie[0]:
        break
      #If the last element has the same match percentage add it too
      elif i+1 == len(percentageMatchedMovieArray) - 1:
        tiedMovies.append(nextMovie)

  reorderedMovies = list(tiedMovies)
  for m in tiedMovies:
    if(str(m[1].year) in originalFileName):
      reorderedMovies.remove(m)
      reorderedMovies.insert(0, m)
  for i in range(0, len(reorderedMovies)):
    percentageMatchedMovieArray[i] = reorderedMovies[i]
  return percentageMatchedMovieArray

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

  #Count how many words are in each title
  lengthOfFirstTitle = len(firstArray)
  lengthOfSecondTitle = len(secondArray)

  #Count the matching words between the two titles
  matchingWordCount = 0
  for word in firstArray:
    if word in secondArray:
      matchingWordCount += 1
      secondArray.remove(word)

  #Calculate the percentage of title match
  percentFirstMatch = float(matchingWordCount) / lengthOfFirstTitle
  percentSecondMatch = float(matchingWordCount) / lengthOfSecondTitle
  return percentFirstMatch * percentSecondMatch
