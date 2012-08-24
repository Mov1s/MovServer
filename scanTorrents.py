import os, sys, re
import string
import commonSettings
from commonMysql import *
from commonHelpers import *
import MySQLdb as mdb
import models.movie as movie
import models.tvSeries as tvSeries
import models.mediaFile as mediaFile
import models.statusCode as statusCode

def main():
	print "Starting Scan"
	systemConf = commonSettings.systemSettings()
	dirConf = commonSettings.directorySettings()

	conn = mdb.connect(systemConf.mysqlServer, systemConf.mysqlUser, systemConf.mysqlPassword, 'movServer')

	pendingItems = 0
	addedShows = []
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
							#Check to see if the movie is in a sub folder
							#if so then do the search based on folder name instead of file name
							if len(root) > len(dirConf.contentSource):
								folderTitle = os.path.basename(root)
								movies = findMovies(folderTitle, newMediaFile)
							else:
								movies = findMovies(file, newMediaFile)

							#Save all of the possible movies
							for m in movies:
								m.save(conn)

							if len(movies) > 0:
								title = movies[0].title
								year = movies[0].year
								moviePath = os.path.join(dirConf.movieDestination, movies[0].formatFileTitle())
								print "Linked " + fullPath + " to movie title \n" + " "*4 + title
								if not os.path.exists(moviePath):
									os.link(fullPath, moviePath)
								movies[0].linkMediaFile(conn)
								movies[0].save(conn)
							else:
								print "No movies for " + fullPath			
					#else:
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
	if pendingItems > 0:
		sendXbmcNotification("Pending Content", str(pendingItems)+" item(s) pending approval.")
	elif len(addedShows) == 1:
		sendXbmcNotification("New Content", addedShows[0]+" was added to the library.")
	elif len(addedShows) > 1:
		sendXbmcNotification("New Content", str(len(addedShows))+" new items were added to the library.")
