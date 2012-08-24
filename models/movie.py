#Model for movie
import os
import commonHelpers
import mediaFile
import statusCode
import MySQLdb as mdb
import commonMysql
import commonSettings

class movie():
	id = None
	title = None
	year = None
	posterUrl = None
	summary = None
	rating = None
	active = None

	#Foreign Keys
	associatedMediaFileId = None

	#Media file for this movie
	associatedMediaFile = None

	def save(self, conn = None):
		if conn == None:
			conn = commonMysql.createConnection()
		cursor = conn.cursor()

		#Update or save associated media file
		if self.associatedMediaFile != None:
			self.associatedMediaFile.save(conn)
			self.associateMediaFile(self.associatedMediaFile)

		#New Movie
		if self.id == None and self.title != None and self.associatedMediaFileId != None:
			try:
				cursor.execute("INSERT INTO Movies (title, year, posterUrl, summary, rating, active, FK_MediaFile_id) VALUES (%s, %s, %s, %s, %s, %s, %s)", (self.title, self.year, self.posterUrl, self.summary, self.rating, self.active, self.associatedMediaFileId))
				conn.commit()
				cursor.execute("SELECT id FROM Movies WHERE title = %s", (self.title))
				result = cursor.fetchall()
				self.id = result[0][0]
			except UnicodeEncodeError:
				print "Unicode error"
		#Update existing movie
		elif self.id != None and self.title != None and self.associatedMediaFileId != None:
			cursor.execute("UPDATE Movies SET title = %s, year = %s, posterUrl = %s, summary = %s, rating = %s, active = %s, FK_MediaFile_id = %s WHERE id = %s", (self.title, self.year, self.posterUrl, self.summary, self.rating, self.active, self.associatedMediaFileId, self.id))
			conn.commit()

		return self

	def associateMediaFile(self, mediaFile):
		if mediaFile != None:
			self.associatedMediaFile = mediaFile
			self.associatedMediaFileId = mediaFile.id
			return self
		else:
			return Exception

	def linkMediaFile(self, conn = None, mediaFile = None):
		if conn == None:
			conn = commonMysql.createConnection()
		if mediaFile != None:
			self.associateMediaFile(mediaFile)

		if self.associatedMediaFile != None:
			mySibblings = getSibblingsOfMovieId(self.id, conn)
			for s in mySibblings:
				s.active = 0
			dirConf = commonSettings.directorySettings()
			moviePath = os.path.join(dirConf.movieDestination, self.formatFileTitle())
			self.associatedMediaFile.linkedPath = moviePath
			self.active = 1
			return self
		else:
			return Exception

	def formatFileTitle(self):
		if self.associatedMediaFile != None:
			origFile = self.associatedMediaFile.path
			return self.title + ' (' + str(self.year) + ')' + commonHelpers.appendHD(origFile) + commonHelpers.appendExtension(origFile)
		else:
			return Exception

	def asJson(self):
		jsonResult = {}
		jsonResult['id'] = self.id
		jsonResult['title'] = self.title
		jsonResult['year'] = self.year
		jsonResult['posterUrl'] = self.posterUrl
		jsonResult['summary'] = self.summary
		jsonResult['rating'] = self.rating
		return jsonResult

#Returns a list of all movies that are attached to a media file with a given path
#path: the path of the media file in question
#conn: the connection to use for the database query, if none provided a default is created
def getByMediaFilePath(path, conn = None):
	if conn == None:
		conn = commonMysql.createConnection()
	cursor = conn.cursor()

	cursor.execute("SELECT * FROM MediaFiles mf LEFT JOIN Movies m ON mf.id = m.FK_MediaFile_id WHERE mf.path = %s", (path))
	if cursor.rowcount == 0:
		return None
	else:
		movieListResult = []
		for title in cursor.fetchall():
			movieInfo = title
			movieResult = createFromArray(movieInfo[3:])
			mediaResult = mediaFile.createFromArray(movieInfo[:3])
			movieResult.associatedMediaFile = mediaResult
			movieListResult.append(movieResult)
		return movieListResult

#Returns a movie with the given id
#movieId: the id of the movie in question
#conn: the connection to use for the database query, if none provided a default is created
def getByMovieId(movieId, conn = None):
	if conn == None:
		conn = commonMysql.createConnection()
	cursor = conn.cursor()

	cursor.execute("SELECT * FROM MediaFiles mf LEFT JOIN Movies m ON mf.id = m.FK_MediaFile_id WHERE m.id = %s", (movieId))
	if cursor.rowcount == 0:
		return None
	else:
		movieInfo = cursor.fetchall()[0]
		movieResult = createFromArray(movieInfo[3:])
		mediaResult = mediaFile.createFromArray(movieInfo[:3])
		movieResult.associatedMediaFile = mediaResult
		return movieResult

#Returns a list of movies that are active links to media files in the library
#conn: the connection to use for the database query, if none provided a default is created
def getFromLibrary(conn = None):
	if conn == None:
		conn = commonMysql.createConnection()
	cursor = conn.cursor()

	cursor.execute("SELECT * FROM MediaFiles mf LEFT JOIN Movies m ON mf.id = m.FK_MediaFile_id WHERE m.active = 1")
	if cursor.rowcount == 0:
		return None
	else:
		movieList = []
		for m in cursor.fetchall():
			movieInfo = m
			movieResult = createFromArray(movieInfo[3:])
			mediaResult = mediaFile.createFromArray(movieInfo[:3])
			movieResult.associatedMediaFile = mediaResult
			movieList.append(movieResult)
		return movieList

#Returns a list of movies that are sibblings to a movie with the given id
#movieId: the id of the movie in question
#conn: the connection to use for the database query, if none provided a default is created
def getSibblingsOfMovieId(movieId, conn = None):
	if conn == None:
		conn = commonMysql.createConnection()
	cursor = conn.cursor()

	cursor.execute("SELECT * FROM Movies m WHERE m.id = %s", (movieId))
	lookupMovieInfo = cursor.fetchall()[0]
	lookupMovie = createFromArray(lookupMovieInfo)

	cursor.execute("SELECT * FROM Movies m WHERE m.FK_MediaFile_id = %s", (lookupMovie.associatedMediaFileId))
	if cursor.rowcount == 0:
		return None
	else:
		movieList = []
		for m in cursor.fetchall():
			movieInfo = m
			movieResult = createFromArray(movieInfo)
			movieList.append(movieResult)
		return movieList

#Create and return a new movie from an array formated by the database
#movieInfoArray: an array formated as a database return containing movie details
def createFromArray(movieInfoArray):
	movieResult = movie()
	movieResult.id = movieInfoArray[0]
	movieResult.title = movieInfoArray[1]
	movieResult.year = movieInfoArray[2]
	movieResult.posterUrl = movieInfoArray[3]
	movieResult.summary = movieInfoArray[4]
	movieResult.rating = movieInfoArray[5]
	movieResult.active = movieInfoArray[6]
	movieResult.associatedMediaFileId = movieInfoArray[7]
	return movieResult

#Create and return a new movie
#title: the title of the new movie, other movie details can be added after creation
#associatedMediaFile: an existing media file that can be associated with the new movie, if none provided the movie is created without a link to a media file
def create(title, associatedMediaFile = None):
	movieResult = movie()
	movieResult.title = title;

	#Add a link to a media file if one is provided, otherwise just create as a generic movie
	if associatedMediaFile != None:
		movieResult.associateMediaFile(associatedMediaFile)
	return movieResult