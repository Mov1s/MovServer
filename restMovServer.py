import bottle
from bottle import route, run, request, abort

import models.movie as movie
import models.mediaFile as mediaFile
import models.series as series
import models.seriesAlias as seriesAlias
import models.episode as episode
import helpers.mediaLinker as mediaLinker

#Movie Routes -------------------------------------------------------------------
#--------------------------------------------------------------------------------
@route('/library/movies', method='GET')
def getLibraryMovies():
	allLibraryMovies = movie.getFromLibrary()
	jsonReturn = {}
	moviesArray = []
	for m in allLibraryMovies:
		moviesArray.append(m.asJson())
	jsonReturn['movies'] = moviesArray
	return jsonReturn

@route('/library/movies/<movieId>', method='GET')
def getLibraryMovieById(movieId):
	requestedMovie = movie.getByMovieId(movieId)
	jsonReturn = {}
	moviesArray = []
	moviesArray.append(requestedMovie.asJson())
	jsonReturn['movies'] = moviesArray
	return jsonReturn

@route('/library/movies/<movieId>/sibblings', method='GET')
def getLibraryMovieSibblings(movieId):
	movieSibblings = movie.getSibblingsOfMovieId(movieId)
	jsonReturn = {}
	moviesArray = []
	for m in movieSibblings:
		moviesArray.append(m.asJson())
	jsonReturn['movies'] = moviesArray
	return jsonReturn

@route('/library/movies/<movieId>/link', method='GET')
def getLibraryMovieCreateLink(movieId):
	linkedMovie = movie.getByMovieId(movieId)
	linkedMediaFile = mediaFile.getByMediaFileId(linkedMovie.associatedMediaFileId)
	mediaLinker.linkMediaFileToMovie(linkedMediaFile, linkedMovie)
	return linkedMovie.asJson()

@route('/library/movies/<movieId>/sibblings', method='POST')
def postLibraryMovie(movieId):
	movieTitle = request.json['title']
	movieYear = request.json['year']

	linkedMovie = movie.getByMovieId(movieId)
	linkedMediaFile = mediaFile.getByMediaFileId(linkedMovie.associatedMediaFileId)
	newMovie = movie.create(movieTitle, movieYear).save()
	mediaLinker.associateMovieWithMediaFile(newMovie, linkedMediaFile)
	return newMovie.asJson()

@route('/library/movies/<movieId>', method='DELETE')
def deleteLibraryMovie(movieId):
	linkedMovie = movie.getByMovieId(movieId)
	linkedMediaFile = mediaFile.getByMediaFileId(linkedMovie.associatedMediaFileId)
	mediaLinker.removeHardLinkForMediaFile(linkedMediaFile)
	return "Successfully Deleted Movie"

#TV Show Routes -----------------------------------------------------------------
#--------------------------------------------------------------------------------
@route('/library/series', method='GET')
def getLibrarySeries():
	allLibrarySeries = series.getFromLibrary()
	jsonReturn = {}
	seriesArray = []
	for s in allLibrarySeries:
		seriesArray.append(s.asJson())
	jsonReturn['series'] = seriesArray
	return jsonReturn

@route('/library/series/<seriesId>', method='GET')
def getLibrarySeries(seriesId):
	aSeries = series.getBySeriesId(seriesId)
	jsonReturn = {}
	seriesArray = [aSeries]
	jsonReturn['series'] = seriesArray
	return jsonReturn

@route('/library/series/<seriesId>/sibblings', method='GET')
def getLibrarySeriesSibblings(seriesId):
	seriesSibblings = series.getSibblingsOfSeriesId(seriesId)
	jsonReturn = {}
	seriesArray = []
	for s in seriesSibblings:
		seriesArray.append(s.asJson())
	jsonReturn['series'] = seriesArray
	return jsonReturn

@route('/library/series/<seriesId>/link', method='GET')
def getLibrarySeriesCreateLink(seriesId):
	linkedSeries = series.getBySeriesId(seriesId)
	linkedEpisodes = episode.getBySeriesAliasId(linkedSeries.associatedSeriesAliasId)
	for lnEp in linkedEpisodes:
		linkedMediaFile = mediaFile.getByMediaFileId(lnEp.associatedMediaFileId)
		mediaLinker.linkMediaFileToSeries(linkedMediaFile, linkedSeries)
	return 'Success'

@route('/library/series/links', method='GET')
def getLibrarySeriesLinks():
	activeSeriesArray = series.getFromLibrary()
	jsonReturn = {}
	for s in activeSeriesArray:
		linkedSeriesAlias = seriesAlias.getBySeriesAliasId(s.associatedSeriesAliasId)
		jsonReturn[s.title] = linkedSeriesAlias.string
	return jsonReturn

@route('/seriesAliases', method='GET')
def getSeriesAliases():
	allSeriesAliases = seriesAlias.get()
	jsonReturn = {}
	seriesAliasArray = []
	for s in allSeriesAliases:
		seriesAliasArray.append(s.asJson())
	jsonReturn['seriesAliases'] = seriesAliasArray
	return jsonReturn

@route('/library/series', method='POST')
def postSeriesAlias():
	seriesTitle = request.json['title']
	seriesAliasId = request.json['associatedSeriesAliasId']

	aSeries = series.create(seriesTitle).save()
	aSeriesAlias = seriesAlias.getBySeriesAliasId(seriesAliasId)
	mediaLinker.associateSeriesWithSeriesAlias(aSeries, aSeriesAlias)
	aSeries = series.getBySeriesId(aSeries.id)
	return aSeries.asJson()

run(host='localhost', port=9000)
