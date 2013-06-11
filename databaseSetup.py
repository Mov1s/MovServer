import string
import MySQLdb as mdb
import helpers.settingsManager as settingsManager

sysSettings = settingsManager.systemSettings()

#Create database
def createDatabase():
	try:
		conn = mdb.connect(sysSettings.mysqlServer, sysSettings.mysqlUser, sysSettings.mysqlPassword)
		cursor = conn.cursor()
		cursor.execute('CREATE DATABASE IF NOT EXISTS movServer')
		conn.close()
	except:
		return False
	return True

#Drop all tables if reset flag is passed
def resetTables():
	try:
		conn = mdb.connect(sysSettings.mysqlServer, sysSettings.mysqlUser, sysSettings.mysqlPassword, 'movServer')
		cursor = conn.cursor()
		cursor.execute('DROP TABLE IF EXISTS Series')
		cursor.execute('DROP TABLE IF EXISTS SeriesAlias')
		cursor.execute('DROP TABLE IF EXISTS Episodes')
		cursor.execute('DROP TABLE IF EXISTS MediaFiles')
		cursor.execute('DROP TABLE IF EXISTS Movies')
		conn.close()
	except:
		return False

#Create tables
def createTables():
	try:
		conn = mdb.connect(sysSettings.mysqlServer, sysSettings.mysqlUser, sysSettings.mysqlPassword, 'movServer')
		cursor = conn.cursor()
		cursor.execute('''
			CREATE TABLE IF NOT EXISTS Series
			(
				id					INT NOT NULL AUTO_INCREMENT,
				title				VARCHAR(1000) NOT NULL,
				active				INT,
				FK_SeriesAlias_id	INT NOT NULL,
				PRIMARY KEY 		(id)
			)''')
		cursor.execute('''
			CREATE TABLE IF NOT EXISTS SeriesAlias
			(
				id					INT NOT NULL AUTO_INCREMENT,
				string				VARCHAR(1000) NOT NULL,
				PRIMARY KEY 		(id)
			)''')
		cursor.execute('''
			CREATE TABLE IF NOT EXISTS Episodes
			(
				id					INT NOT NULL AUTO_INCREMENT,
				season				INT NOT NULL,
				episode				INT NOT NULL,
				FK_SeriesAlias_id	INT,
				FK_MediaFile_id 	INT NOT NULL,
				PRIMARY KEY 		(id)
			)''')
		cursor.execute('''
			CREATE TABLE IF NOT EXISTS MediaFiles
			(
				id					INT NOT NULL AUTO_INCREMENT,
				path				VARCHAR(1000) NOT NULL,
				linkedPath			VARCHAR(1000),
				PRIMARY KEY 		(id)
			)''')
		cursor.execute('''
			CREATE TABLE IF NOT EXISTS Movies
			(
				id					INT NOT NULL AUTO_INCREMENT,
				title				VARCHAR(1000) NOT NULL,
				year				VARCHAR(4),
				posterUrl			VARCHAR(1000),
				summary				VARCHAR(1000),
				rating				VARCHAR(5),
				active				INT,
				FK_MediaFile_id		INT NOT NULL,
				PRIMARY KEY 		(id)
			)''')
		conn.close()
	except:
		return False
	return True

#Try to connect to the database to determine if it is created or not
def databaseExists():
	try:
		mdb.connect(sysSettings.mysqlServer, sysSettings.mysqlUser, sysSettings.mysqlPassword, 'movServer')
		return True
	except:
		return False

#Do first time setup
def firstRun():
	db = createDatabase()
	tables = createTables()
	if db and tables:
		return True
	else:
		return False
