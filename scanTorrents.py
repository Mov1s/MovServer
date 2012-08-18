import os, sys, re
import string
import commonSettings
from commonMysql import *
from commonHelpers import *
import MySQLdb as mdb
import models.movie as movie
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
				tvShowInfo = getSeries(file)
				if tvShowInfo == None:
					if isOfMovieSize(fullPath):
						retrievedMediaFile = mediaFile.getByFilePath(fullPath, conn)
						if retrievedMediaFile == None:
							newMediaFile = mediaFile.createWithPath(fullPath).save(conn)

							f = open('titleResults.txt', 'a')
							#Check to see if the movie is in a sub folder
							#if so then do the search based on folder name instead of file name
							if len(root) > len(dirConf.contentSource):
								folderTitle = os.path.basename(root)
								f.write("File in folder, using the folder name: " + folderTitle + " instead of file name: " + file + "\n")
								print "File in folder, using the folder name: " + folderTitle + " instead of file name: " + file
								titles = findTitles(folderTitle)
							else:
								f.write("Using the file name: " + file + "\n")
								print "Using the file name: " + file
								titles = findTitles(file)

							#Process all the titles
							for t in titles:
								t.associateMediaFile(newMediaFile).save(conn)
							if len(titles) > 0:
								title = titles[0].title
								year = titles[0].year

								moviePath = os.path.join(dirConf.movieDestination, title+ ' (' + str(year) + ')' + appendHD(file)+appendExtension(file))
								
								f.write("\t" + title + "\n")
								print "Linked " + fullPath + " to movie title \n" + " "*4 + title
							else:
								print "No titles for " + fullPath
							f.close()
								#if not os.path.exists(moviePath):
								#	os.link(fullPath, moviePath)
				# else:
				# 	seriesRow = getTvSeries(conn, tvShowInfo[0])
				# 	if seriesRow == None:
				# 		addPendingSeries(conn, tvShowInfo[0])
				# 		pendingItems += 1
				# 	elif seriesRow[3] == 2:
				# 		series = seriesRow[2]
				# 		formatedEpisode = '%s - %sx%s' % (series, tvShowInfo[1], tvShowInfo[2])
				# 		seriesPath = os.path.join(dirConf.tvDestination, series)
				# 		seasonPath = os.path.join(seriesPath, 'Season '+tvShowInfo[1])
				# 		episodePath = os.path.join(seasonPath, formatedEpisode+appendHD(file)+appendExtension(file))
				
				# 		#Check if the series is already in the content
				# 		if not os.path.exists(seriesPath):
				# 			os.makedirs(seriesPath)
				# 		if not os.path.exists(seasonPath):
				# 			os.makedirs(seasonPath)
				# 		if not os.path.exists(episodePath):
				# 			os.link(fullPath, episodePath)
				# 			addedShows.append(formatedEpisode)
	conn.close()
	if pendingItems > 0:
		sendXbmcNotification("Pending Content", str(pendingItems)+" item(s) pending approval.")
	elif len(addedShows) == 1:
		sendXbmcNotification("New Content", addedShows[0]+" was added to the library.")
	elif len(addedShows) > 1:
		sendXbmcNotification("New Content", str(len(addedShows))+" new items were added to the library.")
