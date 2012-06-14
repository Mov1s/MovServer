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

	#Foreign Keys
	statusCode = None
	associatedMediaFileId = None

	#Media file for this movie
	associatedMediaFile = None

	def save(self, conn = None):
		if conn == None:
			conn = commonMysql.createConnection()
		cursor = conn.cursor()

		#New Movie
		if self.id == None and self.statusCode != None and self.title != None:
			try:
				cursor.execute("INSERT INTO Movies (teh_id, title, year, posterUrl, summary, rating, FK_status_code_id, FK_media_file_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (self.tehId, self.title, self.year, self.posterUrl, self.summary, self.rating, self.statusCode, self.associatedMediaFileId))
				conn.commit()
				cursor.execute("SELECT id FROM Movies WHERE title = %s", (self.title))
				result = cursor.fetchall()
				self.id = result[0][0]
			except UnicodeEncodeError:
				print "Unicode error"
		#Update existing movie
		elif self.id != None and self.statusCode != None and self.title != None:
			cursor.execute("UPDATE Movies SET teh_id = %s, title = %s, year = %s, posterUrl = %s, summary = %s, rating = %s, FK_status_code_id = %s, FK_media_file_id = %s WHERE id = %s", (self.tehId, self.title, self.year, self.posterUrl, self.summary, self.rating, self.statusCode, self.associatedMediaFileId, self.id))
			conn.commit()
			if self.associatedMediaFile != None:
				self.associatedMediaFile.save(conn)

		return self

	def finalize(self):
		self.statusCode = statusCode.finalized
		self.associatedMediaFile.statusCode = statusCode.finalized
		return self

	def associateMediaFile(self, mediaFile):
		self.associatedMediaFile = mediaFile
		self.associatedMediaFileId = mediaFile.id
		return self

def getByMediaFilePath(conn, path):
	if conn == None:
		conn = commonMysql.createConnection()
	cursor = conn.cursor()

	cursor.execute("SELECT * FROM MediaFiles mf LEFT JOIN Movies m ON mf.id = m.FK_media_file_id WHERE mf.path = %s", (path))
	if cursor.rowcount == 0:
		return None
	else:
		movieInfo = cursor.fetchall()[0]
		movieResult = createFromArray(movieInfo[3:])
		mediaResult = mediaFile.createFromArray(movieInfo[:3])
		movieResult.associatedMediaFile = mediaResult
		return movieResult

def getByTehMovieId(conn, tehId):
	if conn == None:
		conn = commonMysql.createConnection()
	cursor = conn.cursor()

	cursor.execute("SELECT * FROM Movies m LEFT JOIN MediaFiles mf ON mf.id = m.FK_media_file_id WHERE m.teh_id = %s", (tehId))
	if cursor.rowcount == 0:
		return None
	else:
		movieInfo = cursor.fetchall()[0]
		movieResult = createFromArray(movieInfo[:9])
		mediaResult = mediaFile.createFromArray(movieInfo[9:])
		movieResult.associatedMediaFile = mediaResult
		return movieResult

def createFromArray(movieInfoArray):
	movieResult = movie()
	movieResult.id = movieInfoArray[0]
	movieResult.tehId = movieInfoArray[1]
	movieResult.title = movieInfoArray[2]
	movieResult.year = movieInfoArray[3]
	movieResult.posterUrl = movieInfoArray[4]
	movieResult.summary = movieInfoArray[5]
	movieResult.rating = movieInfoArray[6]
	movieResult.statusCode = movieInfoArray[7]
	movieResult.associatedMediaFileId = movieInfoArray[8]
	return movieResult

def createAsPending(title, associatedMediaFile = None):
	movieResult = movie()
	movieResult.title = title;
	movieResult.statusCode = statusCode.pending

	#Add a link to a media file if one is provided, otherwise just create as a generic movie
	if associatedMediaFile != None:
		movieResult.associatedMediaFileId = associatedMediaFile.id
		movieResult.associatedMediaFile = associatedMediaFile
	return movieResult