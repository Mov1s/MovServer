#Model for movie
import mediaFile
import statusCode
import MySQLdb as mdb
import commonSettings

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
	associatedMediaFile = None

	#Media file for this movie
	mediaFile = None
	
	def __init__(self):
		self.id = None

	def __init__(self, movieInfoArray):
		self.id = movieInfoArray[0]
		self.tehId = movieInfoArray[1]
		self.title = movieInfoArray[2]
		self.year = movieInfoArray[3]
		self.posterUrl = movieInfoArray[4]
		self.summary = movieInfoArray[5]
		self.rating = movieInfoArray[6]
		self.statusCode = movieInfoArray[7]
		self.associatedMediaFile = movieInfoArray[8]

	def save(self, conn = None):
		if conn == None:
			conn = createConnection()
		cursor = conn.cursor()

		#New Movie
		if self.id == None and self.statusCode != None and self.title != None:
			try:
				cursor.execute("INSERT INTO Movies (tehId, title, year, posterUrl, summary, rating, FK_status_code_id, FK_media_file_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (self.tehId, self.title, self.year, self.posterUrl, self.summary, self.rating, self.statusCode, self.associatedMediaFile))
				conn.commit()
				cursor.execute("SELECT id FROM Movies WHERE title = %s", (self.title))
				result = cursor.fetchall()
				self.id = result[0][0]
			except UnicodeEncodeError:
				print "Unicode error"
		#Update existing movie
		elif self.id != None and self.statusCode != None and self.title != None:
			cursor.execute("UPDATE Movies SET tehID = %s, title = %s, year = %s, posterUrl = %s, summary = %s, ratting = %s, FK_status_code_id = %s, FK_media_file_id = %s WHERE id = %s", (self.tehId, self.title, self.year, self.posterUrl, self.summary, self.rating, self.statusCode, self.associatedMediaFile, self.id))
			conn.commit()

		return self.id

def createConnection():
	systemConf = commonSettings.systemSettings()
	conn = mdb.connect(systemConf.mysqlServer, systemConf.mysqlUser, systemConf.mysqlPassword, 'movServer')
	return conn

def getByMediaFilePath(conn, path):
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM MediaFiles mf LEFT JOIN Movies m ON mf.id = m.FK_media_file_id WHERE mf.path = %s", (path))
	if cursor.rowcount == 0:
		return None
	else:
		movieInfo = cursor.fetchall()[0]
		movieResult = movie(movieInfo[3:])
		mediaResult = mediaFile(movieInfo[:3])
		movieResult.mediaFile = mediaResult
		return movieResult

def createAsPending(conn, title, mediaFileId = None):
	movieResult = movie()
	movieResult.title = title;
	movieResult.statusCode = statusCode.pending

	#Add a link to a media file if one is provided, otherwise just create as a generic movie
	if mediaFileId != None:
		movieResult.associatedMediaFile = mediaFileId
	return movieResult