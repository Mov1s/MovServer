#Model for tv series
import mediaFile
import MySQLdb as mdb
import commonMysql

class tvSeries():
	id = None
	title = None
	alias = None

	def save(self, conn = None):
		if conn == None:
			conn = commonMysql.createConnection()
		cursor = conn.cursor()

		#New Series
		if self.id == None and self.title != None:
			try:
				cursor.execute("INSERT INTO TvSeries (title, alias) VALUES (%s, %s)", (self.title, self.alias))
				conn.commit()
				cursor.execute("SELECT id FROM TvSeries WHERE title = %s", (self.title))
				result = cursor.fetchall()
				self.id = result[0][0]
			except UnicodeEncodeError:
				print "Unicode error"
		#Update existing series
		elif self.id != None and self.title != None:
			cursor.execute("UPDATE TvSeries SET title = %s, alias = %s WHERE id = %s", (self.title, self.alias, self.id))
			conn.commit()

		return self

#Returns a tv series that has the given series name
#series: the series name in question
#conn: the connection to use for the database query, if none provided a default is created
def getBySeries(title, conn = None):
	if conn == None:
		conn = commonMysql.createConnection()
	cursor = conn.cursor()

	cursor.execute("SELECT * FROM TvSeries WHERE title = %s", (title))
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
	seriesResult.title = seriesInfoArray[1]
	seriesResult.alias = seriesInfoArray[2]
	return seriesResult

#Create and return a new tv series
#series: the series title of the new tv series, other details can be added after creation
def create(title):
	seriesResult = tvSeries()
	seriesResult.title = title;
	return seriesResult