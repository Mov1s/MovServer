import MySQLdb as mdb
import helpers.settingsManager as settingsManager

#Create connection object
def createConnection():
	systemConf = settingsManager.systemSettings()
	conn = mdb.connect(systemConf.mysqlServer, systemConf.mysqlUser, systemConf.mysqlPassword, 'movServer')
	return conn