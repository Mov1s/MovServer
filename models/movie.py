#Model for movie
import MySQLdb as mdb
import helpers.mysqlConnector as mySql

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

	def save(self, conn = None):
		if conn == None:
			conn = mySql.createConnection()
		cursor = conn.cursor()

		#New Movie
		if self.id == None and self.title != None and self.associatedMediaFileId != None:
			try:
				cursor.execute("INSERT INTO Movies (title, year, posterUrl, summary, rating, active, FK_MediaFile_id) VALUES (%s, %s, %s, %s, %s, %s, %s)", (self.title, self.year, self.posterUrl, self.summary, self.rating, self.active, self.associatedMediaFileId,))
				conn.commit()
				cursor.execute("SELECT id FROM Movies WHERE title = %s AND FK_MediaFile_id = %s", (self.title, self.associatedMediaFileId,))
				result = cursor.fetchall()
				self.id = result[0][0]
			except UnicodeEncodeError:
				print "Unicode error"
		#Update existing movie
		elif self.id != None and self.title != None and self.associatedMediaFileId != None:
			cursor.execute("UPDATE Movies SET title = %s, year = %s, posterUrl = %s, summary = %s, rating = %s, active = %s, FK_MediaFile_id = %s WHERE id = %s", (self.title, self.year, self.posterUrl, self.summary, self.rating, self.active, self.associatedMediaFileId, self.id,))
			conn.commit()

		return self

	def asJson(self):
		jsonResult = {}
		jsonResult['id'] = self.id
		jsonResult['title'] = self.title
		jsonResult['year'] = self.year
		jsonResult['posterUrl'] = self.posterUrl
		jsonResult['summary'] = self.summary
		jsonResult['rating'] = self.rating
		jsonResult['active'] = self.active
		jsonResult['associatedMediaFileId'] = self.associatedMediaFileId
		return jsonResult

#Returns a list of all movies that are attached to a media file with a given path
#mediaFilePath: the path of the media file in question
#conn: the connection to use for the database query, if none provided a default is created
def getByMediaFilePath(mediaFilePath, conn = None):
	if conn == None:
		conn = mySql.createConnection()
	cursor = conn.cursor()

	cursor.execute("SELECT m FROM MediaFiles mf LEFT JOIN Movies m ON mf.id = m.FK_MediaFile_id WHERE mf.path = %s", (mediaFilePath,))
	if cursor.rowcount == 0:
		return []
	else:
		movieListResult = []
		for movieInfoArray in cursor.fetchall():
			movieResult = createFromArray(movieInfoArray)
			movieListResult.append(movieResult)
		return movieListResult

#Returns a list of all movies that are attached to a media file with a given id
#mediaFileId: the id of the media file in question
#conn: the connection to use for the database query, if none provided a default is created
def getByMediaFileId(mediaFileId, conn = None):
	if conn == None:
		conn = mySql.createConnection()
	cursor = conn.cursor()

	cursor.execute("SELECT * FROM Movies m WHERE m.FK_MediaFile_id = %s", (mediaFileId,))
	if cursor.rowcount == 0:
		return []
	else:
		movieListResult = []
		for movieInfoArray in cursor.fetchall():
			movieResult = createFromArray(movieInfoArray)
			movieListResult.append(movieResult)
		return movieListResult

#Returns a movie with the given id
#movieId: the id of the movie in question
#conn: the connection to use for the database query, if none provided a default is created
def getByMovieId(movieId, conn = None):
	if conn == None:
		conn = mySql.createConnection()
	cursor = conn.cursor()

	cursor.execute("SELECT * FROM Movies m WHERE m.id = %s", (movieId,))
	if cursor.rowcount == 0:
		return None
	else:
		movieInfo = cursor.fetchall()[0]
		movieResult = createFromArray(movieInfo)
		return movieResult

#Returns a list of movies that are active links to media files in the library
#conn: the connection to use for the database query, if none provided a default is created
def getFromLibrary(conn = None):
	if conn == None:
		conn = mySql.createConnection()
	cursor = conn.cursor()

	cursor.execute("SELECT * FROM Movies m WHERE m.active = 1")
	if cursor.rowcount == 0:
		return []
	else:
		movieListResult = []
		for movieInfoArray in cursor.fetchall():
			movieResult = createFromArray(movieInfoArray)
			movieListResult.append(movieResult)
		return movieListResult

#Returns a list of movies that are sibblings to a movie with the given id
#movieId: the id of the movie in question
#conn: the connection to use for the database query, if none provided a default is created
def getSibblingsOfMovieId(movieId, conn = None):
	if conn == None:
		conn = mySql.createConnection()
	cursor = conn.cursor()

	cursor.execute("SELECT * FROM Movies m WHERE m.id = %s", (movieId,))
	lookupMovieInfo = cursor.fetchall()[0]
	lookupMovie = createFromArray(lookupMovieInfo)

	cursor.execute("SELECT * FROM Movies m WHERE m.FK_MediaFile_id = %s", (lookupMovie.associatedMediaFileId,))
	if cursor.rowcount == 0:
		return []
	else:
		movieListResult = []
		for movieInfoArray in cursor.fetchall():
			movieResult = createFromArray(movieInfoArray)
			movieListResult.append(movieResult)
		return movieListResult

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
#title: the title of the new movie
#all other movie properties are optional
def create(title, year= None, posterUrl = None, summary = None, rating = None, active = None):
	movieResult = movie()
	movieResult.title = title
	movieResult.year = year
	movieResult.posterUrl = posterUrl
	movieResult.summary = summary
	movieResult.rating = rating
	movieResult.active = active
	return movieResult
