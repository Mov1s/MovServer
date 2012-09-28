import os, sys, re
import string

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
								movies = findMovies(folderTitle)
							else:
								movies = findMovies(file)

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
							seriesArray = findSeries(file)
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



						# retrievedTvSeries = tvSeries.getBySeries(tvShowInfo[0], conn)
						# if retrievedTvSeries == None:
						# 	serieses = findSeries(tvShowInfo[0])
						# 	if len(serieses) > 0:
						# 		print "Adding Tv Series ", serieses[0].alias
						# 		serieses[0].finalize().save(conn)
						# 		pendingItems += 1
						#elif seriesRow[3] == 2:
							# series = seriesRow[2]
							# formatedEpisode = '%s - %sx%s' % (series, tvShowInfo[1], tvShowInfo[2])
							# seriesPath = os.path.join(dirConf.tvDestination, series)
							# seasonPath = os.path.join(seriesPath, 'Season '+tvShowInfo[1])
							# episodePath = os.path.join(seasonPath, formatedEpisode+appendHD(file)+appendExtension(file))
					
							# #Check if the series is already in the content
							# if not os.path.exists(seriesPath):
							# 	os.makedirs(seriesPath)
							# if not os.path.exists(seasonPath):
							# 	os.makedirs(seasonPath)
							# if not os.path.exists(episodePath):
							# 	os.link(fullPath, episodePath)
							# 	addedShows.append(formatedEpisode)
	conn.close()
	if len(addedContent) == 1:
		sendXbmcNotification("New Content", addedContent[0]+" was added to the library.")
	elif len(addedContent) > 1:
		sendXbmcNotification("New Content", str(len(addedContent))+" new items were added to the library.")
