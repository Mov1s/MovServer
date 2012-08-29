#Model for tv series
import MySQLdb as mdb
import helpers.mysqlConnector as mySql

class series():
	id = None
	title = None
	active = None

	#Foreign Keys
	associatedSeriesAliasId = None

	def save(self, conn = None):
		if conn == None:
			conn = mySql.createConnection()
		cursor = conn.cursor()

		#New Series
		if self.id == None and self.title != None and self.associatedSeriesAliasId != None:
			try:
				cursor.execute("INSERT INTO Series (title, FK_SeriesAlias_id) VALUES (%s, %s)", (self.title, self.associatedSeriesAliasId))
				conn.commit()
				cursor.execute("SELECT id FROM Series WHERE title = %s AND FK_SeriesAlias_id = %s", (self.title, self.associatedSeriesAliasId))
				result = cursor.fetchall()
				self.id = result[0][0]
			except UnicodeEncodeError:
				print "Unicode error"
		#Update existing series
		elif self.id != None and self.title != None and self.associatedSeriesAliasId != None:
			cursor.execute("UPDATE Series SET title = %s, active = %s, FK_SeriesAlias_id = %s WHERE id = %s", (self.title, self.active, self.associatedSeriesAliasId, self.id))
			conn.commit()

		return self

#Returns a tv series that has the given id
#seriesId: the series id in question
#conn: the connection to use for the database query, if none provided a default is created
def getBySeriesId(seriesId, conn = None):
	if conn == None:
		conn = mySql.createConnection()
	cursor = conn.cursor()

	cursor.execute("SELECT * FROM Series WHERE id = %s", (seriesId))
	if cursor.rowcount == 0:
		return None
	else:
		seriesInfo = cursor.fetchall()[0]
		seriesResult = createFromArray(seriesInfo)
		return seriesResult

#Returns a list of tv series that for a given seriesAlias id
#seriesAliasId: the series alias id in question
#conn: the connection to use for the database query, if none provided a default is created
def getBySeriesAliasId(seriesAliasId, conn = None):
	if conn == None:
		conn = mySql.createConnection()
	cursor = conn.cursor()

	cursor.execute("SELECT * FROM Series WHERE FK_SeriesAlias_id = %s", (seriesAliasId))
	if cursor.rowcount == 0:
		return None
	else:
		seriesListResult = []
		for seriesInfoArray in cursor.fetchall():
			seriesResult = createFromArray(seriesInfoArray)
			seriesListResult.append(seriesResult)
		return seriesListResult

#Returns a tv series that is the active series for a given seriesAlias id
#seriesAliasId: the series alias id in question
#conn: the connection to use for the database query, if none provided a default is created
def getActiveBySeriesAliasId(seriesAliasId, conn = None):
	if conn == None:
		conn = mySql.createConnection()
	cursor = conn.cursor()

	cursor.execute("SELECT * FROM Series WHERE FK_SeriesAlias_id = %s and active = 1", (seriesAliasId))
	if cursor.rowcount == 0:
		return None
	else:
		seriesInfo = cursor.fetchall()[0]
		seriesResult = createFromArray(seriesInfo)
		return seriesResult

#Create and return a new tv series from an array formated by the database
#seriesInfoArray: an array formated as a database return containing tv series details
def createFromArray(seriesInfoArray):
	seriesResult = series()
	seriesResult.id = seriesInfoArray[0]
	seriesResult.title = seriesInfoArray[1]
	seriesResult.active = seriesInfoArray[2]
	seriesResult.associatedSeriesAliasId = seriesInfoArray[3]
	return seriesResult

#Create and return a new tv series
#title: the series title of the new tv series
#all other series properties are optional
def create(title, active = None):
	seriesResult = series()
	seriesResult.title = title;
	seriesResult.active = active
	return seriesResult