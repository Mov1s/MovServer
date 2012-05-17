import pygtk
pygtk.require('2.0')
import gtk
import os
import commonSettings
import commonMysql

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
		movies = tabMovies(self._notebook, buttonDone)
		tv = tabTv(self._notebook, buttonDone)

		buttonDone.connect_object("clicked", self.destroy, self._parentWindow, None)
		self._notebook.show()
		boxMain.show()
		self._parentWindow.show()

class tabMovies():
	def __init__(self, notebook, buttonDone):
		conn = commonMysql.createConnection()	
		pendingMovies = commonMysql.getPendingMovies(conn)

		table = gtk.Table(2, 2, False)
		tabLabel = gtk.Label("Pending Movies")

		#Left pane for showing all pending movies
		labelLeftPane = gtk.Label("Pending Items")
		labelLeftPane.set_alignment(0, .5)
		scrollLeftPane = gtk.ScrolledWindow()
		sb = scrollLeftPane.get_hscrollbar()
		sb.set_child_visible(False)
		listLeftPane = gtk.List()
		scrollLeftPane.add_with_viewport(listLeftPane)
		table.attach(labelLeftPane, 0, 1, 0, 1, gtk.FILL, gtk.FILL, 1, 1)
		table.attach(scrollLeftPane, 0, 1, 1, 2, gtk.FILL|gtk.EXPAND, gtk.FILL|gtk.EXPAND, 1, 1)
		labelLeftPane.show()
		scrollLeftPane.show()
		listLeftPane.show()

		listLeftPane.connect("selection_changed", self.selectMovie)

		#self._entryScanInterval = gtk.Entry(0)						#Text box for entering the scan interval
		#self._entryScanInterval.set_sensitive(False)

		#Right pane for showing all possible movie titles
		labelRightPane = gtk.Label("Possible Titles")
		labelRightPane.set_alignment(0, .5)
		scrollRightPane = gtk.ScrolledWindow()
		sb = scrollRightPane.get_hscrollbar()
		sb.set_child_visible(False)
		listRightPane = gtk.List()
		scrollRightPane.add_with_viewport(listRightPane)
		table.attach(labelRightPane, 1, 2, 0, 1, gtk.FILL, gtk.FILL, 1, 1)
		table.attach(scrollRightPane, 1, 2, 1, 2, gtk.FILL|gtk.EXPAND, gtk.FILL|gtk.EXPAND, 1, 1)
		labelRightPane.show()
		scrollRightPane.show()
		listRightPane.show()

		listRightPane.connect("selection_changed", self.selectTitle)

		#Add items to list
		itemLabel = gtk.Label("Item 1")
		item = gtk.ListItem()
		item.add(itemLabel)
		itemLabel.show()

		listLeftPane.add(item)
		item.show()
		
		table.show()

		buttonDone.connect("clicked", self.buttonClickDone, None)
		notebook.append_page(table, tabLabel)

	def buttonClickDone(self, widget, data=None):
		print "Clicked the done"

	def selectMovie(self, gtklist, data = None):
		print data

	def selectTitle(self, gtklist, data = None):
		print data
	
class tabTv():	
	def __init__(self, notebook, buttonDone):
		conn = commonMysql.createConnection()
		pendingSeries = commonMysql.getPendingTvSeries(conn)

		table = gtk.Table(3, 1, False)
		tabLabel = gtk.Label("Pending Tv Series")

		#Pane for showing all pending series
		labelPane = gtk.Label("Pending Items")
		labelPane.set_alignment(0, .5)
		scrollPane = gtk.ScrolledWindow()
		sb = scrollPane.get_hscrollbar()
		sb.set_child_visible(False)
		self.listPane = gtk.List()
		scrollPane.add_with_viewport(self.listPane)
		table.attach(labelPane, 0, 1, 0, 1, gtk.FILL, gtk.FILL, 1, 1)
		table.attach(scrollPane, 0, 1, 1, 2, gtk.FILL|gtk.EXPAND, gtk.FILL|gtk.EXPAND, 1, 1)
		labelPane.show()
		scrollPane.show()
		self.listPane.show()

		#Buttons for approve and ignore
		hbox = gtk.HBox(False, 2)
		
		buttonApprove = gtk.Button("Approve")
		buttonIgnore = gtk.Button("Ignore")
		buttonApprove.connect("clicked", self.buttonClickApprove, None)

		hbox.pack_start(buttonApprove, False, False, 2)
		hbox.pack_start(buttonIgnore, False, False, 2)
		buttonApprove.show()
		buttonIgnore.show()
		table.attach(hbox, 0, 1, 2, 3, gtk.FILL, False, 1, 1)
		hbox.show()

		#Add items to list
		for series in pendingSeries:
			item = gtk.ListItem(series[1])
			self.listPane.add(item)
			item.show()
			item.set_data("seriesId", series[0])

		table.show()
		
		buttonDone.connect("clicked", self.buttonClickDone, None)
		notebook.append_page(table, tabLabel)

	def buttonClickDone(self, widget, data=None):
		print "Do"

	def buttonClickApprove(self, widget, data=None):
		selectedItem = self.listPane.get_selection()
		print selectedItem.get_data("seriesId")

def main():
	masterWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
	masterWindow.set_border_width(10)
	go = windowBody(masterWindow)
