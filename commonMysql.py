import MySQLdb as mdb

#Create connection object
def createConnection():
	systemConf = commonSettings.systemSettings()
	conn = mdb.connect(systemConf.mysqlServer, systemConf.mysqlUser, systemConf.mysqlPassword, 'movServer')
	return conn

#TV db functions
def addSeriesAlias(conn, seriesId, newName):
	cursor = conn.cursor()
	cursor.execute("UPDATE TvSeries SET alias = '%s', FileStates_id = 2 WHERE id = %d" % (newName, seriesId))
 	conn.commit()

def addPendingSeries(conn, series):
	cursor = conn.cursor()
	cursor.execute("INSERT INTO TvSeries (series, FileStates_id) VALUES ('%s', 0)" % (series))
	conn.commit()
	
def getTvSeries(conn, series):
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM TvSeries WHERE series = '%s'" % (series))
	if cursor.rowcount == 0:
		return None
	else:
		return cursor.fetchall()[0]
	
#Movie db functions	
def addPendingMovie(conn, path):
	cursor = conn.cursor()
	cursor.execute("INSERT INTO MovieFiles (path, FileStates_id) VALUES ('%s', 0)" % (path))
	conn.commit()
	cursor.execute("SELECT id FROM MovieFiles WHERE path = '%s'" % (path))
	result = cursor.fetchall()
	result = result[0][0]
	return result

def addImdbTitle(conn, title, movieId):
	cursor = conn.cursor()
	try:	
		t = conn.escape_string(title)
		cursor.execute("INSERT INTO MovieTitles (MovieFiles_id, title)	VALUES (%d, '%s')" % (movieId, t))
		conn.commit()
	except UnicodeEncodeError:
		print "Unicode error"

def getMovie(conn, path):
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM MovieFiles mf LEFT JOIN MovieTitles mt ON mf.id = mt.MovieFiles_id WHERE mf.path = '%s'" % (path))
	if cursor.rowcount == 0:
		return None
	else:
		return cursor.fetchall()[0]

def getPendingMovies(conn):
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM MovieFiles WHERE FileStates_id = 0")
	if cursor.rowcount == 0:
		return None
	else
		return cursor.fetchall()

def approveMovie(conn, movieId, titleId):
	cursor = conn.cursor()
	cursor.execute("UPDATE MovieFiles SET FileStates_id = 1 WHERE id = %s" % (movieId))
	cursor.execute("DELETE FROM MovieTitles WHERE MovieFiles_id = %s AND id != %s" % (movieId, titleId))
	conn.commit()

def ignoreMovie(conn, movieId):
	cursor = conn.cursor()
	cursor.execute("UPDATE MovieFiles SET FileStates_id = 3 WHERE id = %s" % (movieId))
	cursor.execute("DELETE FROM MovieTitles WHERE MovieFiles_id = %s" % (movieId))
	conn.commit()

def finalizeMovie(conn, movieId):
	cursor = conn.cursor()
	cursor.execute("UPDATE MovieFiles SET FileStates_id = 2 WHERE id = %d" % (movieId))
	conn.commit()
