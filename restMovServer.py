import bottle
from bottle import route, run, request, abort

import models.movie as movie
import models.mediaFile as mediaFile
import helpers.mediaLinker as mediaLinker

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
	return 'Success'

run(host='localhost', port=8080)