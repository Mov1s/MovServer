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
	print "Starting Scan"
	systemConf = settingsManager.systemSettings()
	dirConf = settingsManager.directorySettings()

	conn = mySql.createConnection()

	addedContent = []
	for root, dirs, files in os.walk(dirConf.contentSource):
		for file in files:
			fullPath = os.path.join(root, file)
			if isVideo(file):
				retrievedMediaFile = mediaFile.getByFilePath(fullPath, conn)
				if retrievedMediaFile == None:
					newMediaFile = mediaFile.createWithPath(fullPath).save(conn)
					#WARNING this should be moved into the TvEpisode class as a static creator
					tvShowInfo = getSeries(file)
					if tvShowInfo == None:
						#File is not a TvEpisode
						if isOfMovieSize(fullPath):
							print file
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
							else:
								print "No movies for " + fullPath			
					else:
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
								print "Linked " + fullPath + " to new series \n" + " "*4 + seriesArray[0].title
							else:
								print "No series for " + fullPath
						else:
							anEpisode = mediaLinker.associateEpisodeWithSeriesAlias(anEpisode, aSeriesAlias)
							aSeries = series.getActiveBySeriesAliasId(aSeriesAlias.id, conn)
							episodeName = mediaLinker.linkMediaFileToSeries(newMediaFile, aSeries)
							addedContent.append(episodeName)
							print "Linked " + fullPath + " to already existing series \n" + " "*4 + aSeries.title

	conn.close()
	if len(addedContent) == 1:
		sendXbmcNotification("New Content", addedContent[0]+" was added to the library.")
	elif len(addedContent) > 1:
		sendXbmcNotification("New Content", str(len(addedContent))+" new items were added to the library.")
