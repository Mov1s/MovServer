import bottle
from bottle import route, run, request, abort
import os, sys, re
import string
import commonSettings
from commonHelpers import *
import MySQLdb as mdb
import models.movie as movie
import models.tvSeries as tvSeries
import models.mediaFile as mediaFile
import models.statusCode as statusCode

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
	linkedMovie.linkMediaFile()
	linkedMovie.save()

	# dirConf = commonSettings.directorySettings()

	# existingMediaFile = mediaFile.getByMediaFileId(1)
	# existingMovie = movie.getByMovieId(5)
	# title = existingMovie.title
	# year = existingMovie.year
	# file = existingMediaFile.path

	# moviePath = os.path.join(dirConf.movieDestination, title+ ' (' + str(year) + ')' + appendHD(file)+appendExtension(file))

	# existingMediaFile.linkedPath = moviePath
	# existingMediaFile.save()
	return 'Success'

run(host='localhost', port=8080)