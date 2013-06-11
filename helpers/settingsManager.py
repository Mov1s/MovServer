import os
import ConfigParser

#Read the config file and prepare it for parsing
home = os.getenv('HOME')
configFile = os.path.join(home, '.movserver.conf')
config = ConfigParser.SafeConfigParser()
config.read(configFile)

#Class for holding directory settings like location of movies
class directorySettings():

	def __init__(self):
		self.pictureSource = config.get('Directories', 'pictureSource')
		self.backdropDestination = config.get('Directories', 'backdropDestination')
		self.movieDestination = config.get('Directories', 'movieDestination')
		self.tvDestination = config.get('Directories', 'tvDestination')
		self.contentSource = config.get('Directories', 'contentSource')
		self.torrentWatchDirectory = config.get('Directories', 'torrentWatchDirectory')

#Class for holding system settings like mysql options or web directories
class systemSettings():

	def __init__(self):
		self.mysqlServer = config.get('System', 'mysqlServer')
		self.mysqlUser = config.get('System', 'mysqlUser')
		self.mysqlPassword = config.get('System', 'mysqlPass')
		self.xbmcPort = int(config.get('System', 'xbmcPort'))
		self.xbmcIp = config.get('System', 'xbmcIp')
		self.tmdbApiKey = config.get('System', 'tmdbApiKey')
		self.apiListenIp = config.get('System', 'apiListenIp')
		self.apiListenPort = int(config.get('System', 'apiListenPort'))
