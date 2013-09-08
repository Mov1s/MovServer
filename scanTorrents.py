import os, sys, re, string

import models.movie as movie
import models.series as series
import models.seriesAlias as seriesAlias
import models.episode as episode
import models.mediaFile as mediaFile
import helpers.mediaApiRepo as mediaApiRepo
import helpers.mediaLinker as mediaLinker
import helpers.mysqlConnector as mySql
import helpers.settingsManager as settingsManager
import helpers.xbmcNotifier as xbmcNotifier
from helpers.mediaFileChecker import *

def main():
	systemConf = settingsManager.systemSettings()
	dirConf = settingsManager.directorySettings()
	conn = mySql.createConnection()

	addedContent = []
	for root, dirs, files in os.walk(dirConf.contentSource):
		for file in files:
			fullPath = os.path.join(root, file)
			if isNewTvEpisode(file, root, conn):
				tvShowInfo = parseFileIntoEpisodeInfo(file)
				newMediaFile = mediaFile.createWithPath(fullPath).save(conn)
				anEpisode = episode.create(tvShowInfo[1], tvShowInfo[2])
				aSeriesAlias = seriesAlias.getBySeriesAliasString(tvShowInfo[0], conn)
				anEpisode = mediaLinker.associateEpisodeWithMediaFile(anEpisode, newMediaFile)
				if aSeriesAlias == None:
					aSeriesAlias = seriesAlias.create(tvShowInfo[0]).save(conn)
					anEpisode = mediaLinker.associateEpisodeWithSeriesAlias(anEpisode, aSeriesAlias)
					seriesArray = mediaApiRepo.findSeriesLikeTitle(file)
					if len(seriesArray) > 0:
						mediaLinker.associateArrayOfSeriesWithSeriesAlias(seriesArray, aSeriesAlias)
						episodeName = mediaLinker.linkMediaFileToSeries(newMediaFile, seriesArray[0])
						addedContent.append(episodeName)
						print file, '  ->  ', episodeName
					else:
						print "\t", "No series for " + file
				else:
					anEpisode = mediaLinker.associateEpisodeWithSeriesAlias(anEpisode, aSeriesAlias)
					aSeries = series.getActiveBySeriesAliasId(aSeriesAlias.id, conn)
					if aSeries:
						episodeName = mediaLinker.linkMediaFileToSeries(newMediaFile, aSeries)
						addedContent.append(episodeName)
						print file, '  ->  ', episodeName
					else:
						print "\t", "No series for " + file
			elif isNewMovie(file, root, conn):
				newMediaFile = mediaFile.createWithPath(fullPath).save(conn)
				#Check to see if the movie is in a sub folder
				#if so then do the search based on folder name instead of file name
				if len(root) > len(dirConf.contentSource):
					folderTitle = os.path.basename(root)
					movies = mediaApiRepo.findMoviesLikeTitle(folderTitle)
				else:
					movies = mediaApiRepo.findMoviesLikeTitle(file)

				if len(movies) > 0:
					mediaLinker.associateArrayOfMoviesWithMediaFile(movies, newMediaFile, conn)
					movieName = mediaLinker.linkMediaFileToMovie(newMediaFile, movies[0], conn)
					addedContent.append(movieName)
					print file, '  ->  ', movieName
				else:
					print "\t", "No movies for " + file			

	conn.close()
	if len(addedContent) == 1:
		xbmcNotifier.sendXbmcNotification("New Content", addedContent[0]+" was added to the library.")
		xbmcNotifier.sendXbmcLibraryUpdate()
	elif len(addedContent) > 1:
		xbmcNotifier.sendXbmcNotification("New Content", str(len(addedContent))+" new items were added to the library.")
		xbmcNotifier.sendXbmcLibraryUpdate()
