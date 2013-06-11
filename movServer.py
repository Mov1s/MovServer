import bottle
import scanTorrents
import databaseSetup
import argparse
import helpers.settingsManager as settingsManager
import helpers.restServer

#Set up the acceptable arguments
parser = argparse.ArgumentParser(description = 'Manage an unruly torrent library')
parser.add_argument('-s, --scan', dest = 'scan', action = 'store_true', help = 'scans your content folders for new media')
parser.add_argument('-r, --reset', dest = 'reset', action = 'store_true', help = 'resets the database tables')
parser.add_argument('-w, --web', dest = 'web', action = 'store_true', help = 'runs the REST API for interacting with your scanned library')
args = parser.parse_args()

#Get the system settings
sysSettings = settingsManager.systemSettings()

#Main program execution 
def main():
	#Install on the first run
	if not databaseSetup.databaseExists():
		print "Creating database tables for first run..."
		success = databaseSetup.firstRun()
		if success:
			print "Successfully created database and tables."
		else:
			print "Something went wrong creating the database or tables, MovServer can not continue :("
			return

	#Perform different actions based on the argument flag
	if args.scan:
		scanTorrents.main()
	elif args.reset:
		databaseSetup.resetTables()
		databaseSetup.createTables()
	elif args.web:
		bottle.run(host = sysSettings.apiListenIp, port = sysSettings.apiListenPort)
	
main()
