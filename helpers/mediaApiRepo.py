import string, tvdb_api, tmdb3
import models.movie as movie
import models.series as series
import helpers.titleHandler as titleHandler
import helpers.settingsManager as settingsManager

def findSeriesLikeTitle(fileName):
  tvdbContext = tvdb_api.Tvdb()
  fileNameArray = titleHandler.returnWellFormatedArrayFromTitle(fileName)

  seriesTitles = {}
  serieses = []
  lastSuccessfulSeries = ''
  for i in range(0, len(fileNameArray)):  
    partialFileName = titleStringFromIndexOfTitleArray(fileNameArray, i)
    try:
      tvdbResult = tvdbContext[partialFileName]
      newSeries = series.create(tvdbResult['seriesname'])
      if not newSeries.title in seriesTitles:
        seriesTitles[newSeries.title] = True
        serieses.append(newSeries)
        lastSuccessfulSeries = partialFileName
    except:
      continue
        
  serieses = titleHandler.orderTvArrayByMatchingSeries(serieses, lastSuccessfulSeries)
  return serieses

def findMoviesLikeTitle(fileName):
  settings = settingsManager.systemSettings()
  tmdb3.set_key(settings.tmdbApiKey)
  fileNameArray = titleHandler.returnWellFormatedArrayFromTitle(fileName)
  
  titles = {}
  movies = []
  lastSuccessfulTitle = ''
  for i in range(0, len(fileNameArray)):
    partialFileName = titleStringFromIndexOfTitleArray(fileNameArray, i)
    tmdbResults = tmdb3.searchMovie(partialFileName)

    loop = 15 if len(tmdbResults) >= 15 else len(tmdbResults)
    for j in range(0, loop):
      try:
        tmdbResult = tmdbResults[j]
        safeMovieTitle = titleHandler.removeWindowsOffendingPunctuation(tmdbResult.title)
        newMovie = movie.create(safeMovieTitle)
        if tmdbResult.releasedate:
          newMovie.year = tmdbResult.releasedate.year
        titleIndex = '{0} {1}'.format(newMovie.title, newMovie.year)
        if not titleIndex in titles:
          titles[titleIndex] = True
          movies.append(newMovie)
      except:
        continue
      lastSuccessfulTitle = partialFileName
  movies = titleHandler.orderMovieArrayByMatchingTitle(movies, lastSuccessfulTitle, fileName)
  return movies

def titleStringFromIndexOfTitleArray(titleArray, index):
  return string.replace(','.join(titleArray[0:index+1]), ',', ' ')
