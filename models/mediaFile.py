#MediaFile model
import statusCode
import MySQLdb as mdb
import commonMysql

class mediaFile():
	id = None
	path = None
	linkedPath = None

	def save(self, conn = None):
		if conn == None:
			conn = commonMysql.createConnection()
		cursor = conn.cursor()

		#New Media File
		if self.id == None and self.path != None:
			try:
				cursor.execute("INSERT INTO MediaFiles (path, linkedPath) VALUES (%s, %s)", (self.path, self.linkedPath))
				conn.commit()
				cursor.execute("SELECT id FROM MediaFiles WHERE path = %s", (self.path))
				result = cursor.fetchall()
				self.id = result[0][0]
			except UnicodeEncodeError:
				print "Unicode error"
		#Update existing movie
		elif self.id != None and self.path != None:
			cursor.execute("UPDATE MediaFiles SET path = %s, linkedPath = %s WHERE id = %s", (self.path, self.linkedPath, self.id))
			conn.commit()

		return self

#Returns a mediaFile with a given path
#path: the path of the media file in question
#conn: the connection to use for the database query, if none provided a default is created
def getByFilePath(path, conn = None):
	if conn == None:
		conn = commonMysql.createConnection()
	cursor = conn.cursor()

	cursor.execute("SELECT * FROM MediaFiles mf WHERE mf.path = %s", (path))
	if cursor.rowcount == 0:
		return None
	else:
		fileInfo = cursor.fetchall()[0]
		movieResult = createFromArray(fileInfo)
		return movieResult

#Returns a mediaFile with a given id
#mediaFileId: the id of the media file in question
#conn: the connection to use for the database query, if none provided a default is created
def getByMediaFileId(mediaFileId, conn = None):
	if conn == None:
		conn = commonMysql.createConnection()
	cursor = conn.cursor()

	cursor.execute("SELECT * FROM MediaFiles mf WHERE mf.id = %s", (mediaFileId))
	if cursor.rowcount == 0:
		return None
	else:
		fileInfo = cursor.fetchall()[0]
		movieResult = createFromArray(fileInfo)
		return movieResult

def createFromArray(mediaFileInfoArray):
	mediaFileResult = mediaFile()
	mediaFileResult.id = mediaFileInfoArray[0]
	mediaFileResult.path = mediaFileInfoArray[1]
	mediaFileResult.linkedPath = mediaFileInfoArray[2]
	return mediaFileResult

def createWithPath(path):
	mediaFileResult = mediaFile()
	mediaFileResult.path = path
	return mediaFileResult