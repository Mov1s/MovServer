#MediaFile model
import statusCode
import commonSettings

class mediaFile():
	id = None
	path = None

	#Foreign Keys
	statusCode = None

	

	def __init__(self, mediaFileInfoArray):
		self.id = movieInfoArray[0]
		self.path = movieInfoArray[1]
		self.statusCode = movieInfoArray[2]

	def __init__(self):
		self.id = None

	def save(self, conn = None):
		if conn == None:
			conn = createConnection()
		cursor = conn.cursor()

		#New Media File
		if self.id == None and self.statusCode != None and self.path != None:
			try:
				cursor.execute("INSERT INTO MediaFiles (path, FK_status_code_id) VALUES (%s, %s)", (self.path, self.statusCode))
				conn.commit()
				cursor.execute("SELECT id FROM MediaFiles WHERE path = %s", (self.path))
				result = cursor.fetchall()
				self.id = result[0][0]
			except UnicodeEncodeError:
				print "Unicode error"
		#Update existing movie
		elif self.id != None and self.statusCode != None and self.path != None:
			cursor.execute("UPDATE MediaFiles SET path = %s, FK_status_code_id = %s WHERE id = %s", (self.path, self.statusCode, self.id))
			conn.commit()

		return self.id

def createConnection():
	systemConf = commonSettings.systemSettings()
	conn = mdb.connect(systemConf.mysqlServer, systemConf.mysqlUser, systemConf.mysqlPassword, 'movServer')
	return conn

def createAsPending(conn, path):
	mediaFileResult = mediaFile()
	mediaFileResult.path = path
	mediaFileResult.statusCode = statusCode.pending
	return mediaFileResult