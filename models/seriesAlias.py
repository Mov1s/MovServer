#Model for tv series alias
import MySQLdb as mdb
import helpers.mysqlConnector as mySql

class seriesAlias():
	id = None
	string = None

	def save(self, conn = None):
		if conn == None:
			conn = mySql.createConnection()
		cursor = conn.cursor()

		#New series alias
		if self.id == None and self.string != None:
			try:
				cursor.execute("INSERT INTO SeriesAlias (string) VALUES (%s)", (self.string,))
				conn.commit()
				cursor.execute("SELECT id FROM SeriesAlias WHERE string = %s", (self.string,))
				result = cursor.fetchall()
				self.id = result[0][0]
			except UnicodeEncodeError:
				print "Unicode error"
		#Update existing series alias
		elif self.id != None and self.string != None:
			cursor.execute("UPDATE SeriesAlias SET string = %s WHERE id = %s", (self.string, self.id,))
			conn.commit()

		return self

	def asJson(self):
		jsonResult = {}
		jsonResult['id'] = self.id
		jsonResult['string'] = self.string
		return jsonResult

#Returns a tv series alias that has the given id
#seriesAliasId: the series alias id in question
#conn: the connection to use for the database query, if none provided a default is created
def getBySeriesAliasId(seriesAliasId, conn = None):
	if conn == None:
		conn = mySql.createConnection()
	cursor = conn.cursor()

	cursor.execute("SELECT * FROM SeriesAlias WHERE id = %s", (seriesAliasId,))
	if cursor.rowcount == 0:
		return None
	else:
		seriesAliasInfo = cursor.fetchall()[0]
		seriesAliasResult = createFromArray(seriesAliasInfo)
		return seriesAliasResult

#Returns a tv series alias that has the given string
#seriesAliasString: the series alias string in question
#conn: the connection to use for the database query, if none provided a default is created
def getBySeriesAliasString(seriesAliasString, conn = None):
	if conn == None:
		conn = mySql.createConnection()
	cursor = conn.cursor()

	cursor.execute("SELECT * FROM SeriesAlias WHERE string = %s", (seriesAliasString,))
	if cursor.rowcount == 0:
		return None
	else:
		seriesAliasInfo = cursor.fetchall()[0]
		seriesAliasResult = createFromArray(seriesAliasInfo)
		return seriesAliasResult

#Returns all tv series aliases
#conn: the connection to use for the database query, if none provided a default is created
def get(conn = None):
	if conn == None:
		conn = mySql.createConnection()
	cursor = conn.cursor()

	cursor.execute("SELECT * FROM SeriesAlias")
	if cursor.rowcount == 0:
		return []
	else:
		seriesAliasListResult = []
		for seriesAliasInfoArray in cursor.fetchall():
			seriesAliasResult = createFromArray(seriesAliasInfoArray)
			seriesAliasListResult.append(seriesAliasResult)
		return seriesAliasListResult

#Create and return a new tv series alias from an array formated by the database
#seriesAliasInfoArray: an array formated as a database return containing tv series alias details
def createFromArray(seriesAliasInfoArray):
	seriesAliasResult = seriesAlias()
	seriesAliasResult.id = seriesAliasInfoArray[0]
	seriesAliasResult.string = seriesAliasInfoArray[1]
	return seriesAliasResult

#Create and return a new tv series alias
#string: the series alias string
def create(string):
	seriesAliasResult = seriesAlias()
	seriesAliasResult.string = string;
	return seriesAliasResult
