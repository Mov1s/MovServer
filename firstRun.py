import pygtk
pygtk.require('2.0')
import gtk
import commonSettings
import databaseSetup
import webSetup
import commonErrorHandling

def showFirstRun(step=0, systemConf = None):
	if step == 0:		#Database instal
		dialog = gtk.Dialog("First Run", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_YES, gtk.RESPONSE_YES, gtk.STOCK_NO, gtk.RESPONSE_NO))
		dialogLabel = gtk.Label("This appears to be your first run,\nwould you like to install the database?")
		dialog.vbox.pack_start(dialogLabel)
		dialogLabel.show()
		response = dialog.run()
		dialog.destroy()
		if response == gtk.RESPONSE_YES:
			conf = commonSettings.systemSettings()
			if showFirstRun(1, conf):
				return True
		return False
	elif step == 1:		#MySQL UN and PW
		dialog = gtk.Dialog("First Run", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_OK, gtk.RESPONSE_OK, gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
		table = gtk.Table(4, 2, False)		
		dialogLabel = gtk.Label("Please provide your MySQL details.")
		table.attach(dialogLabel, 0, 2, 0, 1, gtk.FILL|gtk.EXPAND, False, 1, 1)
		dialogLabel.show()
		#Server address widgets
		labelS = gtk.Label("Server:")
		labelS.set_alignment(0, .5)
		entryS = gtk.Entry(0)
		table.attach(labelS, 0, 1, 1, 2, gtk.FILL, gtk.FILL, 1, 1)
		table.attach(entryS, 1, 2, 1, 2, gtk.FILL|gtk.EXPAND, False, 1, 1)
		labelS.show()
		entryS.show()
		#Username widgets
		labelU = gtk.Label("Username:")
		labelU.set_alignment(0, .5)
		entryU = gtk.Entry(0)
		table.attach(labelU, 0, 1, 2, 3, gtk.FILL, gtk.FILL, 1, 1)
		table.attach(entryU, 1, 2, 2, 3, gtk.FILL|gtk.EXPAND, False, 1, 1)
		labelU.show()
		entryU.show()
		#Password widgets
		labelP = gtk.Label("Password:")
		labelP.set_alignment(0, .5)
		entryP = gtk.Entry(0)
		table.attach(labelP, 0, 1, 3, 4, gtk.FILL, gtk.FILL, 1, 1)
		table.attach(entryP, 1, 2, 3, 4, gtk.FILL|gtk.EXPAND, False, 1, 1)
		labelP.show()
		entryP.show()

		dialog.vbox.pack_start(table)
		table.show()

		response = dialog.run()
		systemConf.mysqlUser = entryU.get_text()
		systemConf.mysqlPassword = entryP.get_text()
		systemConf.mysqlServer = entryS.get_text()
		dialog.destroy()
		if response == gtk.RESPONSE_OK:
			success = databaseSetup.firstRun(systemConf)
			if not success:
				commonErrorHandling.showErrorMessage(None, "There was a problem installing the database,\nplease make sure mySQL is configured properly and\nthe information you provided is correct.")
				if showFirstRun(1, systemConf):
					return True
			else:
				if showFirstRun(10, systemConf):	#Skip web setup and just jump to finalize
					return True
		return False
	elif step == 2:		#Apache web directories
		dialog = gtk.Dialog("First Run", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_OK, gtk.RESPONSE_OK, gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
		table = gtk.Table(3, 2, False)
		dialogLabel = gtk.Label("Please provide your web directories.")
		table.attach(dialogLabel, 0, 2, 0, 1, gtk.FILL|gtk.EXPAND, False, 1, 1)
		dialogLabel.show()
		#CGI-bin widgets
		labelC = gtk.Label("cgi-bin:")
		labelC.set_alignment(0, .5)
		entryC = gtk.Entry(0)
		table.attach(labelC, 0, 1, 1, 2, gtk.FILL, gtk.FILL, 1, 1)
		table.attach(entryC, 1, 2, 1, 2, gtk.FILL|gtk.EXPAND, False, 1, 1)
		labelC.show()
		entryC.show()
		#www widgets
		labelW = gtk.Label("www:")
		labelW.set_alignment(0, .5)
		entryW = gtk.Entry(0)
		table.attach(labelW, 0, 1, 2, 3, gtk.FILL, gtk.FILL, 1, 1)
		table.attach(entryW, 1, 2, 2, 3, gtk.FILL|gtk.EXPAND, False, 1, 1)
		labelW.show()
		entryW.show()
		
		dialog.vbox.pack_start(table)
		table.show()

		response = dialog.run()
		systemConf.cgiDirectory = entryC.get_text()
		systemConf.wwwDirectory = entryW.get_text()
		dialog.destroy()
		if response == gtk.RESPONSE_OK:
			success = webSetup.firstRun(systemConf)
			if not success:
				commonErrorHandling.showErrorMessage(None, 'There was a problem writing files to the web directory,\nplease make sure you have write permission and\nthe information you provided is correct.')
				if showFirstRun(2, systemConf):
					return True
			else:
				if showFirstRun(10, systemConf):
					return True
	
		return False
	elif step == 10:	#Finalize and write settings
		systemConf.writeSettingsToFile()
		print 'Successful first run, settings written'
		return True	
