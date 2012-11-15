import os

#Class for holding directory settings like location of movies
class directorySettings():
	pictureSource = ''
	backdropDestination = ''
	movieDestination = ''
	tvDestination = ''
	contentSource = ''
	torrentWatchDirectory = ''

	def __init__(self):
		self.readSettingsFromFile()

	def readSettingsFromFile(self):
		home = os.getenv('HOME')
		configDir = '.movServer'
		configDir = os.path.join(home, configDir)
		directoryConfigFile = os.path.join(configDir, 'directorySettings.conf')

		if os.path.exists(directoryConfigFile):
			f = open(directoryConfigFile, 'r')
			linesArray = f.readlines()
			for line in linesArray:
				lineParts = line.split('=')
				if(len(lineParts) == 2):
					setting = lineParts[0]
					value = lineParts[1]

					if setting == 'contentSource':
						self.contentSource = value.replace('\n', '').strip()
					elif setting == 'moviesDestination':
						self.movieDestination = value.replace('\n', '').strip()
					elif setting == 'tvDestination':
						self.tvDestination = value.replace('\n', '').strip()
					elif setting == 'pictureSource':
						self.pictureSource = value.replace('\n', '').strip()
					elif setting == 'backdropDestination':
						self.backdropDestination = value.replace('\n', '').strip()
					elif setting == 'torrentWatchDirectory':
						self.torrentWatchDirectory = value.replace('\n', '').strip()
			f.close()
	
	#Write all the settings to 'directorySettings.conf'
	def writeSettingsToFile(self):
		home = os.getenv('HOME')
		configDir = '.movServer'
		configDir = os.path.join(home, configDir)
		configFile = os.path.join(configDir, 'directorySettings.conf')

		f = open(configFile, 'w')
		f.write('contentSource=' + self.contentSource + '\n')
		f.write('moviesDestination=' + self.movieDestination + '\n')
		f.write('tvDestination=' + self.tvDestination + '\n')
		f.write('pictureSource=' + self.pictureSource + '\n')
		f.write('backdropDestination=' + self.backdropDestination + '\n')
		f.write('torrentWatchDirectory=' + self.torrentWatchDirectory + '\n')
		f.close()

#Class for holding system settings like mysql options or web directories
class systemSettings():
	mysqlServer = ''
	mysqlUser = ''
	mysqlPassword = ''
	xbmcPort = 8080
	cgiDirectory = ''
	wwwDirectory = ''

	def __init__(self):
		self.readSettingsFromFile()

	def readSettingsFromFile(self):
		home = os.getenv('HOME')
		configDir = '.movServer'
		configDir = os.path.join(home, configDir)
		systemConfigFile = os.path.join(configDir, 'system.conf')

		if os.path.exists(systemConfigFile):
			f = open(systemConfigFile, 'r')
			linesArray = f.readlines()
			for line in linesArray:
				lineParts = line.split('=')
				if(len(lineParts) == 2):
					setting = lineParts[0]
					value = lineParts[1]
					if setting == 'mysqlUser':
						self.mysqlUser = value.replace('\n', '').strip() if len(value) != 1 else 'root'
					elif setting == 'mysqlPass':
						self.mysqlPassword = value.replace('\n', '').strip()
					elif setting == 'mysqlServer':
						self.mysqlServer = value.replace('\n', '').strip() if len(value) != 1 else 'localhost'
					elif setting == 'cgiDir':
						self.cgiDirectory = value.replace('\n', '').strip() if len(value) != 1 else '/var/www/cgi-bin'
					elif setting == 'wwwDir':
						self.wwwDirectory = value.replace('\n', '').strip() if len(value) != 1 else '/var/www'
					elif setting == 'xbmcPort':
						self.xbmcPort = value.replace('\n', '').strip() if len(value) != 1 else 8080
			f.close()
	
	def writeSettingsToFile(self):
		home = os.getenv('HOME')
		configDir = '.movServer'
		configDir = os.path.join(home, configDir)
		
		if not os.path.exists(configDir):
			os.makedirs(configDir)

		configFile = os.path.join(configDir, 'system.conf')

		f = open(configFile, 'w')
		f.write('mysqlUser=' + self.mysqlUser + '\n')
		f.write('mysqlPass=' + self.mysqlPassword + '\n')
		f.write('mysqlServer=' + self.mysqlServer + '\n')
		f.write('cgiDir=' + self.cgiDirectory + '\n')
		f.write('wwwDir=' + self.wwwDirectory + '\n')
		f.write('xbmcPort=' + str(self.xbmcPort))
		f.close()

#Class for holding scheduling settings like interval to scan content, also can install crontabs
class schedulingSettings():
	scanInterval = None
	generateBackdropsInterval = None
	gatherServerInfoInterval = None
	gatherServerInfoDrives = list()
	_cron = list()		#List of all current crontab entries

	def __init__(self):
		self.readSettingsFromFile()

	def readSettingsFromFile(self):
		home = os.getenv('HOME')
		configDir = '.movServer'
		configDir = os.path.join(home, configDir)
		if not os.path.exists(configDir):
			return False

		crontabFile = os.path.join(configDir, 'crontab')
		os.system('crontab -l > ' + crontabFile)

		f = open(crontabFile, 'r')
		self._cron = f.readlines()
		for i in self._cron:
			words = i.split()
			if len(words) >= 6 and words[5] == 'movserver' and words[6] == '-s':
				self.scanInterval = words[0].split('/')[1].strip()
			elif len(words) >= 6 and words[5] == 'movserver' and words[6] == '-b':
				self.generateBackdropsInterval = words[2].split('/')[1].strip()
			elif len(words) >= 6 and words[5] == 'movserver' and words[6] == '-g':
				self.gatherServerInfoInterval = words[1].split('/')[1].strip()
		f.close()
	
	#Write all the settings to 'directorySettings.conf'
	def writeSettingsToFile(self):
		home = os.getenv('HOME')
		configDir = '.movServer'
		configDir = os.path.join(home, configDir)
		crontabFile = os.path.join(configDir, 'crontab')

		f = open(crontabFile, 'w')
		#Write all cron settings back into place and delete current movServer settings
		for i in self._cron:
			words = i.split()
			if len(words) >= 6 and words[5] == 'movserver' and words[6] == '-s':
				i = ''
			elif len(words) >= 6 and words[5] == 'movserver' and words[6] == '-b':
				i = ''
			elif len(words) >= 6 and words[5] == 'movserver' and words[6] == '-g':
				i = ''

			f.write(i)

		#Write movServer settings into the file
		if self.scanInterval != None:
			f.write('*/' + self.scanInterval + ' * * * * movserver -s >/dev/null 2>&1\n')
		if self.generateBackdropsInterval != None:
			f.write('* * */' + self.generateBackdropsInterval + ' * * movserver -b >/dev/null 2>&1\n')
		if self.gatherServerInfoInterval != None:
			f.write('* */' + self.gatherServerInfoInterval + ' * * * movserver -g >/dev/null 2>&1\n')

		f.close()

		newCron = os.system('crontab ' + crontabFile)
