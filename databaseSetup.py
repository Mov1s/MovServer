import string
import MySQLdb as mdb

#Create database
def createDatabase(settings):
	try:
		conn = mdb.connect(settings.mysqlServer, settings.mysqlUser, settings.mysqlPassword)
		cursor = conn.cursor()
		cursor.execute('CREATE DATABASE IF NOT EXISTS movServer')
		conn.close()
	except:
		return False
	return True

#Drop all tables if reset flag is passed
def resetTables(settings):
	try:
		conn = mdb.connect(settings.mysqlServer, settings.mysqlUser, settings.mysqlPassword, 'movServer')
		cursor = conn.cursor()
		cursor.execute('DROP TABLE IF EXISTS TvSeries')
		cursor.execute('DROP TABLE IF EXISTS StatusCodes')
		cursor.execute('DROP TABLE IF EXISTS MediaFiles')
		cursor.execute('DROP TABLE IF EXISTS Movies')
		conn.close()
	except:
		return False

#Create tables
def createTables(settings):
	try:
		conn = mdb.connect(settings.mysqlServer, settings.mysqlUser, settings.mysqlPassword, 'movServer')
		cursor = conn.cursor()
		cursor.execute('''
			CREATE TABLE IF NOT EXISTS TvSeries
			(
				id					INT NOT NULL AUTO_INCREMENT,
				series				VARCHAR(1000) NOT NULL,
				alias				VARCHAR(1000),
				FileStates_id		INT NOT NULL,
				PRIMARY KEY 		(id)
			)''')
		cursor.execute('''
			CREATE TABLE IF NOT EXISTS StatusCodes
			(
				id					INT NOT NULL AUTO_INCREMENT,
				name				VARCHAR(50),
				PRIMARY KEY 		(id)
			)''')
		cursor.execute('''
			CREATE TABLE IF NOT EXISTS MediaFiles
			(
				id					INT NOT NULL AUTO_INCREMENT,
				path				VARCHAR(1000) NOT NULL,
				FK_status_code_id	INT NOT NULL,
				PRIMARY KEY 		(id)
			)''')
		cursor.execute('''
			CREATE TABLE IF NOT EXISTS Movies
			(
				id					INT NOT NULL AUTO_INCREMENT,
				teh_id				INT,
				title				VARCHAR(1000) NOT NULL,
				year				VARCHAR(4),
				posterUrl			VARCHAR(1000),
				summary				VARCHAR(1000),
				rating				VARCHAR(5),
				FK_media_file_id	INT,
				PRIMARY KEY 		(id)
			)''')
		conn.close()
	except:
		return False
	return True

#Do first time setup
def firstRun(settings):
	db = createDatabase(settings)
	resetTables(settings)
	tables = createTables(settings)
	if db and tables:
		return True
	else:
		return False