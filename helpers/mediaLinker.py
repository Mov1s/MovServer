import os
import models.movie as movie
import models.mediaFile as mediaFile
import models.episode as episode
import models.series as series
import models.seriesAlias as seriesAlias
import helpers.mysqlConnector as mySql
import helpers.settingsManager as settingsManager

#Association functions ----------------------------------------------------------
#--------------------------------------------------------------------------------
def associateMovieWithMediaFile(aMovie, aMediaFile, conn = None):
	if conn == None:
		conn = mySql.createConnection()
	cursor = conn.cursor()

	aMovie.associatedMediaFileId = aMediaFile.id
	aMovie.save(conn) 
	return aMovie 

def associateArrayOfMoviesWithMediaFile(aMovieArray, aMediaFile, conn = None):
	if conn == None:
		conn = mySql.createConnection()
	cursor = conn.cursor()

	for m in aMovieArray:
		associateMovieWithMediaFile(m, aMediaFile, conn)

def associateEpisodeWithMediaFile(anEpisode, aMediaFile, conn = None):
	if conn == None:
		conn = mySql.createConnection()
	cursor = conn.cursor()

	anEpisode.associatedMediaFileId = aMediaFile.id
	anEpisode.save(conn)
	return anEpisode

def associateEpisodeWithSeriesAlias(anEpisode, aSeriesAlias, conn = None):
	if conn == None:
		conn = mySql.createConnection()
	cursor = conn.cursor()

	anEpisode.associatedSeriesAliasId = aSeriesAlias.id
	anEpisode.save(conn)
	return anEpisode

def associateSeriesWithSeriesAlias(aSeries, aSeriesAlias, conn = None):
	if conn == None:
		conn = mySql.createConnection()
	cursor = conn.cursor()

	aSeries.associatedSeriesAliasId = aSeriesAlias.id
	aSeries.save(conn)
	return aSeries

def associateArrayOfSeriesWithSeriesAlias(aSeriesArray, aSeriesAlias, conn = None):
	if conn == None:
		conn = mySql.createConnection()
	cursor = conn.cursor()

	for s in aSeriesArray:
		associateSeriesWithSeriesAlias(s, aSeriesAlias, conn)

#Linker functions ---------------------------------------------------------------
#--------------------------------------------------------------------------------
def linkMediaFileToMovie(aMediaFile, aMovie, conn = None):
	if conn == None:
		conn = mySql.createConnection()
	cursor = conn.cursor()

	dirConf = settingsManager.directorySettings()

	#Set the proper movie as 'Active'
	movieArray = movie.getByMediaFileId(aMediaFile.id, conn)
	for m in movieArray:
		m.active = 0
		if m.id == aMovie.id:
			m.active = 1
		m.save(conn)

	#Delete the existing linked file if there is one
	removeHardLinkForMediaFile(aMediaFile)

	#Generate a new linked file name and path and update the media file accordingly
	movieFileName = generateHardLinkNameFromMediaFileAndMovie(aMediaFile, aMovie)
	moviePath = os.path.join(dirConf.movieDestination, movieFileName)
	aMediaFile.linkedPath = moviePath
	aMediaFile.save(conn)

	#Create the new link
	createHardLinkForMediaFile(aMediaFile)

	return movieFileName

def linkMediaFileToSeries(aMediaFile, aSeries, conn = None):
	if conn == None:
		conn = mySql.createConnection()
	cursor = conn.cursor()

	dirConf = settingsManager.directorySettings()

	#Get all the episode information needed to do the linking
	anEpisode = episode.getByMediaFileId(aMediaFile.id, conn)
	aSeriesAlias = seriesAlias.getBySeriesAliasId(anEpisode.associatedSeriesAliasId, conn)

	#Set the proper series as 'Active'
	seriesArray = series.getBySeriesAliasId(aSeriesAlias.id, conn)
	for s in seriesArray:
		s.active = 0
		if s.id == aSeries.id:
			s.active = 1
		s.save(conn)

	#Delete the existing linked file if there is one
	removeHardLinkForMediaFile(aMediaFile)
	removeSeasonFolderIfEmptyForMediaFile(aMediaFile)
	removeSeriesFolderIfEmptyForMediaFile(aMediaFile)

	#Generate a new linked file name and path and update the media file accordingly
	episodeFileName = generateHardLinkNameFromMediaFileAndEpisodeAndSeries(aMediaFile, anEpisode, aSeries)
	seasonPath = generateSeasonPathFromEpisodeAndSeries(anEpisode, aSeries)
	episodePath = os.path.join(seasonPath, episodeFileName)
	aMediaFile.linkedPath = episodePath
	aMediaFile.save(conn)

	#Create the new link
	createSeriesFolderForMediaFile(aMediaFile)
	createSeasonFolderForMediaFile(aMediaFile)
	createHardLinkForMediaFile(aMediaFile)

	return episodeFileName

def removeHardLinkForMediaFile(aMediaFile):
	if aMediaFile.linkedPath != None:
		moviePath = aMediaFile.linkedPath
		if os.path.exists(moviePath):
			os.remove(moviePath)
	else:
		return Exception

def removeSeasonFolderIfEmptyForMediaFile(aMediaFile):
	if aMediaFile.linkedPath != None:
		seasonPath = os.path.dirname(aMediaFile.linkedPath)
		if os.path.exists(seasonPath):
			if os.listdir(seasonPath) == []:
				os.rmdir(seasonPath)

def removeSeriesFolderIfEmptyForMediaFile(aMediaFile):
	if aMediaFile.linkedPath != None:
		seasonPath = os.path.dirname(aMediaFile.linkedPath)
		seriesPath = os.path.dirname(seasonPath)
		if os.path.exists(seriesPath):
			if os.listdir(seriesPath) == []:
				os.rmdir(seriesPath)

def createHardLinkForMediaFile(aMediaFile):
	if aMediaFile.linkedPath != None:
		fullPath = aMediaFile.path
		moviePath = aMediaFile.linkedPath
		if not os.path.exists(moviePath):
			os.link(fullPath, moviePath)
	else:
		return Exception

def createSeriesFolderForMediaFile(aMediaFile):
	if aMediaFile.linkedPath != None:
		seasonPath = os.path.dirname(aMediaFile.linkedPath)
		seriesPath = os.path.dirname(seasonPath)
		if not os.path.exists(seriesPath):
			os.makedirs(seriesPath)

def createSeasonFolderForMediaFile(aMediaFile):
	if aMediaFile.linkedPath != None:
		seasonPath = os.path.dirname(aMediaFile.linkedPath)
		if not os.path.exists(seasonPath):
			os.makedirs(seasonPath)

#File naming functions ----------------------------------------------------------
#--------------------------------------------------------------------------------
def generateHardLinkNameFromMediaFileAndMovie(aMediaFile, aMovie):
	if aMediaFile != None:
		#Get the parts of the file name i need
		title = aMovie.title
		year = aMovie.year
		quality = generateQualityFromMediaFile(aMediaFile)
		extension = generateExtensionFromMediaFile(aMediaFile)

		#Genereate the file name skeleton depending on if the quality is HD
		fileNameSkeleton = '{0} ({1}){3}' if quality == '' else '{0} ({1}) [{2}]{3}'

		return fileNameSkeleton.format(title, year, quality, extension)
	else:
		return Exception

def generateHardLinkNameFromMediaFileAndEpisodeAndSeries(aMediaFile, anEpisode, aSeries):
	if aMediaFile != None:
		#Get the parts of the file name i need
		series = aSeries.title
		season = anEpisode.season
		episode = anEpisode.episode
		quality = generateQualityFromMediaFile(aMediaFile)
		extension = generateExtensionFromMediaFile(aMediaFile)

		#Generate the file name skeleton
		episodeSkeleton = '0{2}' if anEpisode.episode <= 9 else '{2}'
		seasonSkeleton = '0{1}' if anEpisode.season <= 9 else '{1}'
		qualitySkeleton = '{3}' if quality == '' else ' [{3}]'
		fileNameSkeleton = '{0} - '+seasonSkeleton+'x'+episodeSkeleton+qualitySkeleton+'{4}'

		return fileNameSkeleton.format(series, season, episode, quality, extension)
	else:
		return Exception

def generateSeasonPathFromEpisodeAndSeries(anEpisode, aSeries):
	dirConf = settingsManager.directorySettings()
	seriesPath = os.path.join(dirConf.tvDestination, aSeries.title)

	seasonFolderSkeleton = 'Season 0{0}' if anEpisode.season <= 9 else 'Season {0}'

	seasonPath = os.path.join(seriesPath, seasonFolderSkeleton.format(anEpisode.season))
	return seasonPath

def generateQualityFromMediaFile(aMediaFile):
	hd = ''
	path = aMediaFile.path
	if (path.find('720') != -1):
		hd ='720'
	elif (path.find('1080') != -1):
		hd = '1080'
	return hd

def generateExtensionFromMediaFile(aMediaFile):
	path = aMediaFile.path
	return path[path.rfind('.'):]