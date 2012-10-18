import os, sys, re, string

from commonHelpers import *
import models.movie as movie
import models.series as series
import models.seriesAlias as seriesAlias
import models.episode as episode
import models.mediaFile as mediaFile
import helpers.mediaLinker as mediaLinker
import helpers.mysqlConnector as mySql
import helpers.settingsManager as settingsManager

def main():
	systemConf = settingsManager.systemSettings()
	dirConf = settingsManager.directorySettings()
	conn = mySql.createConnection()

	addedContent = []
	for root, dirs, files in os.walk(dirConf.contentSource):
		for file in files:
			fullPath = os.path.join(root, file)
			if isNewTvEpisode(file, root, conn):
				print file
				tvShowInfo = getSeries(file)
				newMediaFile = mediaFile.createWithPath(fullPath).save(conn)
				anEpisode = episode.create(tvShowInfo[1], tvShowInfo[2])
				aSeriesAlias = seriesAlias.getBySeriesAliasString(tvShowInfo[0], conn)
				anEpisode = mediaLinker.associateEpisodeWithMediaFile(anEpisode, newMediaFile)
				if aSeriesAlias == None:
					aSeriesAlias = seriesAlias.create(tvShowInfo[0]).save(conn)
					anEpisode = mediaLinker.associateEpisodeWithSeriesAlias(anEpisode, aSeriesAlias)
					seriesArray = findImdbSeriesLikeTitle(file)
					if len(seriesArray) > 0:
						mediaLinker.associateArrayOfSeriesWithSeriesAlias(seriesArray, aSeriesAlias)
						episodeName = mediaLinker.linkMediaFileToSeries(newMediaFile, seriesArray[0])
						addedContent.append(episodeName)
						print "\t", episodeName
					else:
						print "\t", "No series for " + file
				else:
					anEpisode = mediaLinker.associateEpisodeWithSeriesAlias(anEpisode, aSeriesAlias)
					aSeries = series.getActiveBySeriesAliasId(aSeriesAlias.id, conn)
					episodeName = mediaLinker.linkMediaFileToSeries(newMediaFile, aSeries)
					addedContent.append(episodeName)
					print "\t", episodeName
			elif isNewMovie(file, root, conn):
				print file
				newMediaFile = mediaFile.createWithPath(fullPath).save(conn)
				#Check to see if the movie is in a sub folder
				#if so then do the search based on folder name instead of file name
				if len(root) > len(dirConf.contentSource):
					folderTitle = os.path.basename(root)
					movies = findImdbMoviesLikeTitle(folderTitle)
				else:
					movies = findImdbMoviesLikeTitle(file)

				if len(movies) > 0:
					mediaLinker.associateArrayOfMoviesWithMediaFile(movies, newMediaFile, conn)
					movieName = mediaLinker.linkMediaFileToMovie(newMediaFile, movies[0], conn)
					addedContent.append(movieName)
					print "\t", movieName
				else:
					print "\t", "No movies for " + file			

	conn.close()
	if len(addedContent) == 1:
		sendXbmcNotification("New Content", addedContent[0]+" was added to the library.")
	elif len(addedContent) > 1:
		sendXbmcNotification("New Content", str(len(addedContent))+" new items were added to the library.")

#Helpers for checking media type ------------------------------------------------
#--------------------------------------------------------------------------------
def isNewTvEpisode(file, root, conn = None):
	fullPath = os.path.join(root, file)
	isVideo = fileIsVideo(fullPath)
	isNewMediaFile = (mediaFile.getByFilePath(fullPath, conn) == None)
	isTvEpisode = (getSeries(file) != None)
	isOfEpisodeSize = fileIsOfEpisodeSize(fullPath)
	return isVideo and isNewMediaFile and isTvEpisode and isOfEpisodeSize

def isNewMovie(file, root, conn = None):
	fullPath = os.path.join(root, file)
	isVideo = fileIsVideo(fullPath)
	isNewMediaFile = (mediaFile.getByFilePath(fullPath, conn) == None)
	isNotTvEpisode = (getSeries(file) == None)
	isOfMovieSize = fileIsOfMovieSize(fullPath)
	return isVideo and isNewMediaFile and isNotTvEpisode and isOfMovieSize

def fileIsVideo(fileName):
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

def fileIsOfMovieSize(fileName):
	#return True
	result = False
	if os.path.getsize(fileName) >= 629145600:
		result = True
	return result

def fileIsOfEpisodeSize(fileName):
	#return True
	result = False
	if os.path.getsize(fileName) >= 104857600:
		result = True
	return result