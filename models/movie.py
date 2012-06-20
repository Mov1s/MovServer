#Model for movie
import mediaFile
import statusCode
import MySQLdb as mdb
import commonMysql

class movie():
	id = None
	tehId = None
	title = None
	year = None
	posterUrl = None
	summary = None
	rating = None

	#Fields pulled from associatedMediaFile
	statusCode = None
	path = None

	#Foreign Keys
	associatedMediaFileId = None

	#Media file for this movie
	associatedMediaFile = None

	def save(self, conn = None):
		if conn == None:
			conn = commonMysql.createConnection()
		cursor = conn.cursor()

		#New Movie
		if self.id == None and self.title != None:
			try:
				cursor.execute("INSERT INTO Movies (teh_id, title, year, posterUrl, summary, rating, FK_media_file_id) VALUES (%s, %s, %s, %s, %s, %s, %s)", (self.tehId, self.title, self.year, self.posterUrl, self.summary, self.rating, self.associatedMediaFileId))
				conn.commit()
				cursor.execute("SELECT id FROM Movies WHERE title = %s", (self.title))
				result = cursor.fetchall()
				self.id = result[0][0]
			except UnicodeEncodeError:
				print "Unicode error"
		#Update existing movie
		elif self.id != None and self.statusCode != None and self.title != None:
			cursor.execute("UPDATE Movies SET teh_id = %s, title = %s, year = %s, posterUrl = %s, summary = %s, rating = %s, FK_media_file_id = %s WHERE id = %s", (self.tehId, self.title, self.year, self.posterUrl, self.summary, self.rating, self.associatedMediaFileId, self.id))
			conn.commit()

		#Update or save associated media file
		if self.associatedMediaFile != None:
			self.associatedMediaFile.save(conn)

		return self

	def finalize(self):
		if self.associateMediaFile != None:
			self.associatedMediaFile.statusCode = statusCode.finalized
			return self
		else:
			return Exception

	def associateMediaFile(self, mediaFile):
		if mediaFile.id != None:
			self.associatedMediaFile = mediaFile
			self.associatedMediaFileId = mediaFile.id
			return self
		else:
			return Exception

#Returns a list of all movies that are attached to a media file with a given path
#path: the path of the media file in question
#conn: the connection to use for the database query, if none provided a default is created
def getByMediaFilePath(path, conn = None):
	if conn == None:
		conn = commonMysql.createConnection()
	cursor = conn.cursor()

	cursor.execute("SELECT * FROM MediaFiles mf LEFT JOIN Movies m ON mf.id = m.FK_media_file_id WHERE mf.path = %s", (path))
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

#Returns a single movie that has the given tehConnection ID
#tehId: the tehConnection ID in question
#conn: the connection to use for the database query, if none provided a default is created 
def getByTehMovieId(tehId, conn = None):
	if conn == None:
		conn = commonMysql.createConnection()
	cursor = conn.cursor()

	cursor.execute("SELECT * FROM Movies m LEFT JOIN MediaFiles mf ON mf.id = m.FK_media_file_id WHERE m.teh_id = %s", (tehId))
	if cursor.rowcount == 0:
		return None
	else:
		movieInfo = cursor.fetchall()[0]
		movieResult = createFromArray(movieInfo[:8])
		mediaResult = mediaFile.createFromArray(movieInfo[8:])
		movieResult.associatedMediaFile = mediaResult
		return movieResult

#Create and return a new movie from an array formated by the database
#movieInfoArray: an array formated as a database return containing movie details
def createFromArray(movieInfoArray):
	movieResult = movie()
	movieResult.id = movieInfoArray[0]
	movieResult.tehId = movieInfoArray[1]
	movieResult.title = movieInfoArray[2]
	movieResult.year = movieInfoArray[3]
	movieResult.posterUrl = movieInfoArray[4]
	movieResult.summary = movieInfoArray[5]
	movieResult.rating = movieInfoArray[6]
	movieResult.associatedMediaFileId = movieInfoArray[7]
	return movieResult

#Create and return a new movie as a pending movie file
#title: the title of the new movie, other movie details can be added after creation
#associatedMediaFile: an existing media file that can be associated with the new pending movie, if none provided the movie is created without a link to a media file
def createAsPending(title, associatedMediaFile = None):
	movieResult = movie()
	movieResult.title = title;

	#Add a link to a media file if one is provided, otherwise just create as a generic movie
	if associatedMediaFile != None:
		movieResult.associatedMediaFileId = associatedMediaFile.id
		movieResult.associatedMediaFile = associatedMediaFile
	return movieResult