import pygtk
pygtk.require('2.0')
import gtk

def showErrorMessage(parentWindow, message):
	dialog = gtk.Dialog("Problem", parentWindow, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_OK, gtk.RESPONSE_OK))
	dialogLabel = gtk.Label(message)
	dialog.vbox.pack_start(dialogLabel)
	dialogLabel.show()
	response = dialog.run()
	dialog.destroy()
	if response == gtk.RESPONSE_OK:
		return True
	return False
