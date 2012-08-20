#Model for tv series
import mediaFile
import statusCode
import MySQLdb as mdb
import commonMysql

class tvSeries():
	id = None
	series = None
	alias = None

	#Fields pulled from associatedMediaFile
	statusCode = None

	def save(self, conn = None):
		if conn == None:
			conn = commonMysql.createConnection()
		cursor = conn.cursor()

		#New Series
		if self.id == None and self.series != None and self.statusCode != None:
			try:
				cursor.execute("INSERT INTO TvSeries (series, alias, FileStates_id) VALUES (%s, %s, %s)", (self.series, self.alias, self.statusCode))
				conn.commit()
				cursor.execute("SELECT id FROM TvSeries WHERE series = %s", (self.series))
				result = cursor.fetchall()
				self.id = result[0][0]
			except UnicodeEncodeError:
				print "Unicode error"
		#Update existing series
		elif self.id != None and self.statusCode != None and self.series != None:
			cursor.execute("UPDATE TvSeries SET series = %s, alias = %s, FileStates_id = %s WHERE id = %s", (self.series, self.alias, self.statusCode, self.id))
			conn.commit()

		#Update or save associated media file
		#if self.associatedMediaFile != None:
		#	self.associatedMediaFile.save(conn)

		return self

	def finalize(self):
		self.statusCode = statusCode.finalized
		return self

#Returns a tv series that has the given series name
#series: the series name in question
#conn: the connection to use for the database query, if none provided a default is created
def getBySeries(series, conn = None):
	if conn == None:
		conn = commonMysql.createConnection()
	cursor = conn.cursor()

	cursor.execute("SELECT * FROM TvSeries WHERE series = %s", (series))
	if cursor.rowcount == 0:
		return None
	else:
		seriesInfo = cursor.fetchall()[0]
		seriesResult = createFromArray(seriesInfo)
		return seriesResult

#Create and return a new tv series from an array formated by the database
#seriesInfoArray: an array formated as a database return containing tv series details
def createFromArray(seriesInfoArray):
	seriesResult = tvSeries()
	seriesResult.id = seriesInfoArray[0]
	seriesResult.series = seriesInfoArray[1]
	seriesResult.alias = seriesInfoArray[2]
	seriesResult.statusCode = seriesInfoArray[3]
	return seriesResult

#Create and return a new tv series
#series: the series title of the new tv series, other details can be added after creation
def create(series):
	seriesResult = tvSeries()
	seriesResult.series = series;
	seriesResult.statusCode = statusCode.pending
	return seriesResult