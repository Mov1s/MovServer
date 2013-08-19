import os, string, re
import models.mediaFile as mediaFile

#Helpers for checking media type ------------------------------------------------
#--------------------------------------------------------------------------------
def isNewTvEpisode(file, root, conn = None):
	fullPath = os.path.join(root, file)
	isVideo = fileIsVideo(fullPath)
	isNewMediaFile = (mediaFile.getByFilePath(fullPath, conn) == None)
	isTvEpisode = (parseFileIntoEpisodeInfo(file) != None)
	isOfEpisodeSize = fileIsOfEpisodeSize(fullPath)
	return isVideo and isNewMediaFile and isTvEpisode and isOfEpisodeSize

def isNewMovie(file, root, conn = None):
	fullPath = os.path.join(root, file)
	isVideo = fileIsVideo(fullPath)
	isNewMediaFile = (mediaFile.getByFilePath(fullPath, conn) == None)
	isNotTvEpisode = (parseFileIntoEpisodeInfo(file) == None)
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

def parseFileIntoEpisodeInfo(fileName):
	parsed = re.search("([Ss][\d]+[Xx_\.\s]?[Ee][Pp]?[\d]+)|([_\.\s][\d]+[Xx][\d]+[_\.\s])", fileName)
	if parsed == None:
		return None
	series =  fileName[:parsed.start(0)]
	for c in string.punctuation:
		series = series.replace(c, ' ')
	series = series.lower()
	series = string.capwords(series)
	
	parsedNumbers = re.findall("\d+", parsed.group(0))
	season = parsedNumbers[0]
	if len(season) == 1:
		season = '0'+season
	episode = parsedNumbers[1]
	if len(episode) ==1:
		episode = '0'+episode

	return [series, season, episode]
