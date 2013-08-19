import MySQLdb as mdb
import helpers.settingsManager as settingsManager

OPEN_CONNECTION = None

#Create connection object
def createConnection():
	global OPEN_CONNECTION
	if OPEN_CONNECTION == None:
		systemConf = settingsManager.systemSettings()
		OPEN_CONNECTION = mdb.connect(systemConf.mysqlServer, systemConf.mysqlUser, systemConf.mysqlPassword, 'movServer')
	return OPEN_CONNECTION