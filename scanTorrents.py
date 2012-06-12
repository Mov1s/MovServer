import os, sys, re
import string
import commonSettings
import movCrawler
from commonMysql import *
from commonHelpers import *
import MySQLdb as mdb

def main():
	#Import torrents from movCrawler if running
	movCrawler.importTorrents()
	
	systemConf = commonSettings.systemSettings()
	dirConf = commonSettings.directorySettings()

	conn = mdb.connect(systemConf.mysqlServer, systemConf.mysqlUser, systemConf.mysqlPassword, 'movServer')

	pendingItems = 0
	addedShows = []
	for root, dirs, files in os.walk(dirConf.contentSource):
		for file in files:
			fullPath = os.path.join(root, file)
			if isVideo(file):
				tvShowInfo = getSeries(file)
				if tvShowInfo == None:
					if isOfMovieSize(fullPath):
						movieRow = getMovie(conn, fullPath)
						if movieRow == None:
							movieId = addPendingMovie(conn, fullPath)
							pendingItems += 1
							titles = findTitles(file)
							for t in titles:
								addImdbTitle(conn, t, movieId)
						elif movieRow[2] == 1:
							title = movieRow[5]
							moviePath = os.path.join(dirConf.movieDestination, title+appendHD(file)+appendExtension(file))
							if not os.path.exists(moviePath):
								print fullPath
								print moviePath
								os.link(fullPath, moviePath)
							finalizeMovie(conn, movieRow[0], movieRow[3])
				else:
					seriesRow = getTvSeries(conn, tvShowInfo[0])
					if seriesRow == None:
						addPendingSeries(conn, tvShowInfo[0])
						pendingItems += 1
					elif seriesRow[3] == 2:
						series = seriesRow[2]
						formatedEpisode = '%s - %sx%s' % (series, tvShowInfo[1], tvShowInfo[2])
						seriesPath = os.path.join(dirConf.tvDestination, series)
						seasonPath = os.path.join(seriesPath, 'Season '+tvShowInfo[1])
						episodePath = os.path.join(seasonPath, formatedEpisode+appendHD(file)+appendExtension(file))
				
						#Check if the series is already in the content
						if not os.path.exists(seriesPath):
							os.makedirs(seriesPath)
						if not os.path.exists(seasonPath):
							os.makedirs(seasonPath)
						if not os.path.exists(episodePath):
							os.link(fullPath, episodePath)
							addedShows.append(formatedEpisode)
	conn.close()
	if pendingItems > 0:
		sendXbmcNotification("Pending Content", str(pendingItems)+" item(s) pending approval.")
	elif len(addedShows) == 1:
		sendXbmcNotification("New Content", addedShows[0]+" was added to the library.")
	elif len(addedShows) > 1:
		sendXbmcNotification("New Content", str(len(addedShows))+" new items were added to the library.")
