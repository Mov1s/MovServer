import shutil
import os

def installWebFiles(settings):
	toDir = os.path.join(settings.wwwDirectory, 'movServer')

	try:
		if not os.path.exists(toDir):
			os.mkdir(toDir)
		toDir = toDir.replace(' ', '\ ')
		os.system('tar -xvf /usr/share/movServer/webFrontEndFiles.tar.gz -C ' + toDir)
	except:
		return False
	return True

def installCgiFiles(settings):
	toDir = settings.cgiDirectory

	try:
		if not os.path.exists(toDir):
			os.mkdir(toDir)
		toDir = toDir.replace(' ', '\ ')
		os.system('tar -xvf /usr/share/movServer/cgiBinFiles.tar.gz -C ' + toDir)
	except:
		return False
	return True

def firstRun(settings):
	webInstalled = installWebFiles(settings)
	cgiInstalled = installCgiFiles(settings)

	if webInstalled and cgiInstalled:
		return True
	return False
