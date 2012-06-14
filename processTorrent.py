import os, sys, re
import string
import commonSettings
from commonMysql import *
from commonHelpers import *
import MySQLdb as mdb
import models.movie as movie
import models.mediaFile as mediaFile
import models.statusCode as statusCode


#The tied file name (torrent name)
argTorName = sys.argv[1]

#The torrent root directory
argRootDir = sys.argv[2]

systemConf = commonSettings.systemSettings()
dirConf = commonSettings.directorySettings()

conn = mdb.connect(systemConf.mysqlServer, systemConf.mysqlUser, systemConf.mysqlPassword, 'movServer')

pendingItems = 0
addedMedia = []
for root, dirs, files in os.walk(argRootDir):
	for file in files:
		fullPath = os.path.join(root, file)
		if isVideo(file):
			if isOfMovieSize(fullPath):
				torrentName = argTorName[argTorName.rfind('/')+1:]
				isManaged = torrentName.find('_managed_by_movserver.torrent') != -1
				movieRow = movie.getByMediaFilePath(conn, fullPath)
				if movieRow == None:
					if isManaged:
						#Managed movie
						tehMovieId = torrentName[:torrentName.find('_')]
						pendingMediaFile = mediaFile.createAsPending(fullPath).save(conn)
						managedMovie = movie.getByTehMovieId(conn, tehMovieId)							
						managedMovie.associateMediaFile(pendingMediaFile)

						addedMedia.append(managedMovie.title)
						managedMovie.finalize().save(conn)

						moviePath = os.path.join(dirConf.movieDestination, managedMovie.title+appendHD(file)+appendExtension(file))
						if not os.path.exists(moviePath):
							os.link(fullPath, moviePath)
					else:
						#Unmanaged movie
						pendingMediaFile = mediaFile.createAsPending(fullPath).save(conn)
						pendingItems += 1
						titles = findTitles(file)
						for t in titles:
							movie.createAsPending(t, pendingMediaFile).save(conn)
			#else:
				#Is tv show
				#TODO

conn.close()
if pendingItems > 0:
	sendXbmcNotification("Pending Content", str(pendingItems)+" item(s) pending approval.")
elif len(addedMedia) == 1:
	sendXbmcNotification("New Content", addedMedia[0]+" was added to the library.")
elif len(addedMedia) > 1:
	sendXbmcNotification("New Content", str(len(addedMedia))+" new items were added to the library.")
