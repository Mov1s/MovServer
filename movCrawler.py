#movCrawler functions
import shutil, os
import commonSettings

def importTorrents():
	dirSettings = commonSettings.directorySettings()
	src = dirSettings.crawlerTorrentSource
	dst = dirSettings.torrentWatchDirectory

	if src != '':
		for root, dirs, files in os.walk(src):
			for torrent in files:
				srcTorrent = os.path.join(root, torrent)
				dstTorrent = os.path.join(dst, torrent)
				shutil.move(srcTorrent, dstTorrent)