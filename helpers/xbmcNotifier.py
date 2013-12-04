import httplib
import string
import helpers.settingsManager as settingsManager

def sendXbmcNotification(title, message):
	title = string.replace(title, ' ', '%20')
	message = string.replace(message, ' ', '%20')
	try:
		settings = settingsManager.systemSettings()
		conn = httplib.HTTPConnection(settings.xbmcIp, settings.xbmcPort, timeout=1)
		conn.connect()
		conn.request('GET', '/xbmcCmds/xbmcHttp?command=ExecBuiltIn(Notification('+title+','+message+'))')
		r = conn.getresponse()
		conn.close()
	except:
		print "Had a problem sending message to XBMC"

def sendXbmcLibraryUpdate():
	try:
		settings = settingsManager.systemSettings()
		conn = httplib.HTTPConnection(settings.xbmcIp, settings.xbmcPort, timeout=1)
		conn.connect()
		conn.request('GET', '/xbmcCmds/xbmcHttp?command=ExecBuiltIn(UpdateLibrary(video))')
		r = conn.getresponse()
		conn.close()
	except:
		print "Had a problem updating XBMC's library"
