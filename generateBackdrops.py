import sys, os
import helpers.settingsManager as settingsManager
from PIL import Image

def main():
	dirConf = settingsManager.directorySettings()
	pictureDestination = dirConf.backdropDestination
	pictureSource = dirConf.pictureSource

	for filename in os.listdir(pictureSource):
		if os.path.isdir(os.path.join(pictureSource, filename)) != True and os.path.exists(os.path.join(pictureDestination, filename)) == False:
			try:
				im = Image.open(os.path.join(pictureSource, filename))
				res = im.size
				ratio = float(res[1])/res[0]

				if ratio > .5525 and ratio < .635 and res[0] > 1000:
					newY = res[0]*.5625
					padY = (res[1] - newY)/2
					image = im.crop((0,int(padY),res[0],res[1]-int(padY)))
					image = image.resize((1920,1080))
					image.save(os.path.join(pictureDestination, filename))
			except IOError:
				pass
