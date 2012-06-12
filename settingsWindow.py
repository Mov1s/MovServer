import pygtk
pygtk.require('2.0')
import gtk
import os
import commonSettings

class windowBody(object):
	def destroy(self, widget, data=None):
		print "destroy event occured"
		gtk.main_quit()

	def __init__(self, parentWindow):
		self._parentWindow = parentWindow
		self._parentWindow.connect("destroy", self.destroy)
		self._parentWindow.set_title("MovServer")

		boxMain = gtk.VBox(False, 2)
		boxBottom = gtk.HBox(False, 2)

		self._notebook = gtk.Notebook()
		boxMain.pack_start(self._notebook, True, True, 2)

		buttonDone = gtk.Button("Done")
		boxBottom.pack_end(buttonDone, False, False, 2)

		self._parentWindow.add(boxMain)

		boxMain.pack_end(boxBottom, False, False, 2)
	
		buttonDone.show()
		boxBottom.show()

		#Create tabs
		settings = tabSettings(self._notebook, buttonDone)
		scheduling = tabScheduling(self._notebook, buttonDone)

		buttonDone.connect_object("clicked", self.destroy, self._parentWindow, None)
		self._notebook.show()
		boxMain.show()
		self._parentWindow.show()

class tabScheduling():
	def __init__(self, notebook, buttonDone):
		self._settings = commonSettings.schedulingSettings()
		
		table = gtk.Table(7, 2, False)
		tabLabel = gtk.Label("Scheduling")

		#Options for scanning for new torrents
		self._checkScan = gtk.CheckButton("Scan Torrents", False)			#Checkbox for enable/disable scanning
		self._checkScan.connect("toggled", self.scanToggle, None)
		labelScanInterval = gtk.Label("Scan Interval (min):")				#Label for the interval text box
		labelScanInterval.set_alignment(0, .5)
		self._entryScanInterval = gtk.Entry(0)						#Text box for entering the scan interval
		self._entryScanInterval.set_sensitive(False)
		table.attach(self._checkScan, 0, 1, 0, 1, gtk.FILL, gtk.FILL, 1, 1)
		table.attach(labelScanInterval, 0, 1, 1, 2, gtk.FILL, gtk.FILL, 1, 1)
		table.attach(self._entryScanInterval, 1, 2, 1, 2, gtk.FILL|gtk.EXPAND, False, 1, 1)
		self._checkScan.show()
		labelScanInterval.show()
		self._entryScanInterval.show()

		#Options for generating XBMC backdrops
		self._checkBackdrops = gtk.CheckButton("Generate XBMC Backdrops", False)		#Checkbox for enable/disable generating picture backdrops
		self._checkBackdrops.connect("toggled", self.backdropsToggle, None)
		labelBackdropsInterval = gtk.Label("Generate Interval (days):")				#Label for the interval text box
		labelBackdropsInterval.set_alignment(0, .5)
		self._entryBackdropsInterval = gtk.Entry(0)						#Text box for entering the generating interval
		self._entryBackdropsInterval.set_sensitive(False)
		table.attach(self._checkBackdrops, 0, 1, 2, 3, gtk.FILL, gtk.FILL, 1, 1)
		table.attach(labelBackdropsInterval, 0, 1, 3, 4, gtk.FILL, gtk.FILL, 1, 1)
		table.attach(self._entryBackdropsInterval, 1, 2, 3, 4, gtk.FILL|gtk.EXPAND, False, 1, 1)
		self._checkBackdrops.show()
		labelBackdropsInterval.show()
		self._entryBackdropsInterval.show()

		#Options for gathering server info
		self._checkGather = gtk.CheckButton("Gather Server Info", False)			#Checkbox for enable/disable gathering server information
		self._checkGather.connect("toggled", self.gatherToggle, None)
		labelGatherInterval = gtk.Label("Gather Interval (hours):")				#Label for the interval text box
		labelGatherInterval.set_alignment(0, .5)
		self._entryGatherInterval = gtk.Entry(0)						#Text box for entering the gathering interval
		self._entryGatherInterval.set_sensitive(False)
		labelGatherDrives = gtk.Label("Drives to Probe:")				#Label for the drives text box
		labelGatherDrives.set_alignment(0, .5)
		self._entryGatherDrives = gtk.Entry(0)						#Text box for entering the drives to probe
		self._entryGatherDrives.set_sensitive(False)
		table.attach(self._checkGather, 0, 1, 4, 5, gtk.FILL, gtk.FILL, 1, 1)
		table.attach(labelGatherInterval, 0, 1, 5, 6, gtk.FILL, gtk.FILL, 1, 1)
		table.attach(self._entryGatherInterval, 1, 2, 5, 6, gtk.FILL|gtk.EXPAND, False, 1, 1)
		table.attach(labelGatherDrives, 0, 1, 6, 7, gtk.FILL, gtk.FILL, 1, 1)
		table.attach(self._entryGatherDrives, 1, 2, 6, 7, gtk.FILL|gtk.EXPAND, False, 1, 1)
		self._checkGather.show()
		labelGatherInterval.show()
		labelGatherDrives.show()
		self._entryGatherDrives.show()
		self._entryGatherInterval.show()

		self.readSettings()
		table.show()

		buttonDone.connect("clicked", self.buttonClickDone, None)
		notebook.append_page(table, tabLabel)

	def buttonClickDone(self, widget, data=None):
		self.writeSettings()

	def scanToggle(self, widget, data):
		if self._checkScan.get_active() == False:		#Check box not checked so disable text entry
			self._entryScanInterval.set_sensitive(False)
		else:
			self._entryScanInterval.set_sensitive(True)

	def backdropsToggle(self, widget, data):
		if self._checkBackdrops.get_active() == False:		#Check box not checked so disable text entry
			self._entryBackdropsInterval.set_sensitive(False)
		else:
			self._entryBackdropsInterval.set_sensitive(True)
	
	def gatherToggle(self, widget, data):
		if self._checkGather.get_active() == False:		#Check box not checked so disable text entry
			self._entryGatherInterval.set_sensitive(False)
			self._entryGatherDrives.set_sensitive(False)
		else:
			self._entryGatherInterval.set_sensitive(True)
			self._entryGatherDrives.set_sensitive(True)

	def readSettings(self):
		if self._settings.scanInterval != None:
			self._entryScanInterval.set_text(self._settings.scanInterval)
			self._checkScan.set_active(True)
			self._entryScanInterval.set_sensitive(True)
		if self._settings.generateBackdropsInterval != None:
			self._entryBackdropsInterval.set_text(self._settings.generateBackdropsInterval)
			self._checkBackdrops.set_active(True)
			self._entryBackdropsInterval.set_sensitive(True)
		if self._settings.gatherServerInfoInterval != None:
			self._entryGatherInterval.set_text(self._settings.gatherServerInfoInterval)
			self._checkGather.set_active(True)
			self._entryGatherInterval.set_sensitive(True)
			self._entryGatherDrives.set_sensitive(True)

	def writeSettings(self):
		if self._checkScan.get_active() == True and self._entryScanInterval.get_text() != '':
			self._settings.scanInterval = self._entryScanInterval.get_text()
		else:
			self._settings.scanInterval = None

		if self._checkBackdrops.get_active() == True and self._entryBackdropsInterval.get_text() != '':
			self._settings.generateBackdropsInterval = self._entryBackdropsInterval.get_text()
		else:
			self._settings.generateBackdropsInterval = None

		if self._checkGather.get_active() == True and self._entryGatherInterval.get_text() != '':
			self._settings.gatherServerInfoInterval = self._entryGatherInterval.get_text()
		else:
			self._settings.gatherServerInfoInterval = None

		self._settings.writeSettingsToFile()

class tabSettings():	
	def __init__(self, notebook, buttonDone):
		self._settings = commonSettings.directorySettings()

		table = gtk.Table(7, 2, False)
		tabLabel = gtk.Label("Directory Settings")

		#Content for the "Completed Torrent Directory"
		labelContent = gtk.Label("Completed Torrent Directory:")
		labelContent.set_alignment(0, .5)
		self._entryContent = gtk.Entry(0)
		table.attach(labelContent, 0, 1, 0, 1, gtk.FILL, gtk.FILL, 1, 1)
		table.attach(self._entryContent, 1, 2, 0, 1, gtk.FILL|gtk.EXPAND, False, 1, 1)
		labelContent.show()
		self._entryContent.show()

		#Content for the "Movies Directory"
		labelMovies = gtk.Label("Movies Destination Directory:")
		labelMovies.set_alignment(0, .5)
		self._entryMovies = gtk.Entry(0)
		table.attach(labelMovies, 0, 1, 1, 2, gtk.FILL, gtk.FILL, 1, 1)
		table.attach(self._entryMovies, 1, 2, 1, 2, gtk.FILL|gtk.EXPAND, False, 1, 1)
		labelMovies.show()
		self._entryMovies.show()

		#Content for the "TV Directory"
		labelTv = gtk.Label("TV Destination Directory:")
		labelTv.set_alignment(0, .5)
		self._entryTv = gtk.Entry(0)
		table.attach(labelTv, 0, 1, 2, 3, gtk.FILL, gtk.FILL, 1, 1)
		table.attach(self._entryTv, 1, 2, 2, 3, gtk.FILL|gtk.EXPAND, False, 1, 1)
		labelTv.show()
		self._entryTv.show()

		#Content for the "Picture Source Directory"
		labelPicture = gtk.Label("Picture Source Directory:")
		labelPicture.set_alignment(0, .5)
		self._entryPicture = gtk.Entry(0)
		table.attach(labelPicture, 0, 1, 3, 4, gtk.FILL, gtk.FILL, 1, 1)
		table.attach(self._entryPicture, 1, 2, 3, 4, gtk.FILL|gtk.EXPAND, False, 1, 1)
		labelPicture.show()
		self._entryPicture.show()

		#Content for the "XBMC Backdrop Directory"
		labelBackdrop = gtk.Label("XBMC Backdrop Directory:")
		labelBackdrop.set_alignment(0, .5)
		self._entryBackdrop = gtk.Entry(0)
		table.attach(labelBackdrop, 0, 1, 4, 5, gtk.FILL, gtk.FILL, 1, 1)
		table.attach(self._entryBackdrop, 1, 2, 4, 5, gtk.FILL|gtk.EXPAND, False, 1, 1)
		labelBackdrop.show()
		self._entryBackdrop.show()

		#Content for the "MovCrawler Install Directory"
		labelMovCrawler = gtk.Label("MovCrawler Install Directory:")
		labelMovCrawler.set_alignment(0, .5)
		self._entryMovCrawler = gtk.Entry(0)
		table.attach(labelMovCrawler, 0, 1, 5, 6, gtk.FILL, gtk.FILL, 1, 1)
		table.attach(self._entryMovCrawler, 1, 2, 5, 6, gtk.FILL|gtk.EXPAND, False, 1, 1)
		labelMovCrawler.show()
		self._entryMovCrawler.show()

		#Content for the "Watch Torrent Directory"
		labelWatch = gtk.Label("Watch Torrent Directory:")
		labelWatch.set_alignment(0, .5)
		self._entryWatch = gtk.Entry(0)
		table.attach(labelWatch, 0, 1, 6, 7, gtk.FILL, gtk.FILL, 1, 1)
		table.attach(self._entryWatch, 1, 2, 6, 7, gtk.FILL|gtk.EXPAND, False, 1, 1)
		labelWatch.show()
		self._entryWatch.show()

		self.readSettings()
		table.show()
		buttonDone.connect("clicked", self.buttonClickDone, None)
		notebook.append_page(table, tabLabel)

	def buttonClickDone(self, widget, data=None):
		self.writeSettings()

	def readSettings(self):		
		self._entryContent.set_text(self._settings.contentSource)
		self._entryMovies.set_text(self._settings.movieDestination)
		self._entryTv.set_text(self._settings.tvDestination)
		self._entryPicture.set_text(self._settings.pictureSource)
		self._entryBackdrop.set_text(self._settings.backdropDestination)
		self._entryMovCrawler.set_text(self._settings.crawlerTorrentSource)
		self._entryWatch.set_text(self._settings.torrentWatchDirectory)

	def writeSettings(self):
		self._settings.contentSource = self._entryContent.get_text()
		self._settings.movieDestination = self._entryMovies.get_text()
		self._settings.tvDestination = self._entryTv.get_text()
		self._settings.pictureSource = self._entryPicture.get_text()
		self._settings.backdropDestination = self._entryBackdrop.get_text()
		self._settings.crawlerTorrentSource = self._entryMovCrawler.get_text()
		self._settings.torrentWatchDirectory = self._entryWatch.get_text()
		self._settings.writeSettingsToFile()

def main():
	masterWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
	masterWindow.set_border_width(10)
	go = windowBody(masterWindow)
