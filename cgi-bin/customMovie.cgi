#!/usr/bin/python2

import cgi, cgitb
import sys, os 
sys.path.insert(0, os.path.dirname('/srv/scripts/'))
from movTorrentCommon.movTorrentSettings import *
from movTorrentCommon.movTorrentMySQL import *
from movTorrentCommon.movTorrentCommon import *
import MySQLdb as mdb

#print "Content-type:text/html\r\n\r\n"
print "Location:../index.php\r\n\r\n"

conn = mdb.connect(movServer, movUser, movPassword, 'movTorrent')
form = cgi.FieldStorage()
movieId = int(form.getvalue('mid'))
raw = form.getvalue('raw')

titles = findTitlesRaw(raw)
for t in titles:
	addImdbTitle(conn, t, movieId)
conn.close()
