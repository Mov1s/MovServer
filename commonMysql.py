import MySQLdb as mdb
import commonSettings
import sys

#Create connection object
def createConnection():
	systemConf = commonSettings.systemSettings()
	conn = mdb.connect(systemConf.mysqlServer, systemConf.mysqlUser, systemConf.mysqlPassword, 'movServer')
	return conn

#TV db functions
def addSeriesAlias(conn, seriesId, newName):
	cursor = conn.cursor()
	cursor.execute("UPDATE TvSeries SET alias = %s, FileStates_id = 2 WHERE id = %d", (newName, seriesId))
 	conn.commit()

def addPendingSeries(conn, series):
	cursor = conn.cursor()
	cursor.execute("INSERT INTO TvSeries (series, FileStates_id) VALUES (%s, 0)", (series))
	conn.commit()

def getTvSeries(conn, series):
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM TvSeries WHERE series = %s", (series))
	if cursor.rowcount == 0:
		return None
	else:
		return cursor.fetchall()[0]

def getPendingTvSeries(conn):
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM TvSeries WHERE FileStates_id = 0")
	if cursor.rowcount == 0:
		return None
	else:
		return cursor.fetchall()

#Movie db functions
def addPendingMovie(conn, path):
	cursor = conn.cursor()
	cursor.execute("INSERT INTO MediaFiles (path, FK_status_code_id) VALUES (%s, 0)", (path))
	conn.commit()
	cursor.execute("SELECT id FROM MediaFiles WHERE path = %s", (path))
	result = cursor.fetchall()
	result = result[0][0]
	return result

def addImdbTitle(conn, title, mediaFileId):
	cursor = conn.cursor()
	try:
		t = conn.escape_string(title)
		cursor.execute("INSERT INTO Movies (FK_media_file_id, FK_status_code_id, title) VALUES (%s, 0, %s)", (mediaFileId, t))
		conn.commit()
	except UnicodeEncodeError:
		print "Unicode error"

def getMovieTitle(conn, movieId):
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM Movies WHERE id = %s", (movieId))
	if cursor.rowcount == 0:
		return None
	else:
		return cursor.fetchall()[0]

def getPendingMovies(conn):
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM MediaFiles WHERE FK_status_code_id = 0")
	if cursor.rowcount == 0:
		return None
	else:
		return cursor.fetchall()

def finalizeMovie(conn, mediaFileId, movieId):
	cursor = conn.cursor()
	cursor.execute("UPDATE MediaFiles SET FK_status_code_id = 2 WHERE id = %s", (mediaFileId))
	cursor.execute("UPDATE Movies SET FK_status_code_id = 2, FK_media_file_id = %s WHERE id = %s", (mediaFileId, movieId))
	conn.commit()