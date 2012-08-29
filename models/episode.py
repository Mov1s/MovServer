#Model for tv episode
import MySQLdb as mdb
import helpers.mysqlConnector as mySql

class episode():
	id = None
	season = None
	episode = None

	#Foreign Keys
	associatedSeriesAliasId = None
	associatedMediaFileId = None

	def save(self, conn = None):
		if conn == None:
			conn = mySql.createConnection()
		cursor = conn.cursor()

		#New Episode
		if self.id == None and self.season != None and self.episode != None and self.associatedMediaFileId != None:
			try:
				cursor.execute("INSERT INTO Episodes (season, episode, FK_SeriesAlias_id, FK_MediaFile_id) VALUES (%s, %s, %s, %s)", (self.season, self.episode, self.associatedSeriesAliasId, self.associatedMediaFileId))
				conn.commit()
				cursor.execute("SELECT id FROM Episodes WHERE FK_MediaFile_id = %s", (self.associatedMediaFileId))
				result = cursor.fetchall()
				self.id = result[0][0]
			except UnicodeEncodeError:
				print "Unicode error"
		#Update existing episode
		elif self.id != None and self.season != None and self.episode != None and self.associatedMediaFileId != None:
			cursor.execute("UPDATE Episodes SET season = %s, episode = %s, FK_SeriesAlias_id = %s, FK_MediaFile_id = %s WHERE id = %s", (self.season, self.episode, self.associatedSeriesAliasId, self.associatedMediaFileId, self.id))
			conn.commit()

		return self

#Returns a tv episode that has the given id
#episodeId: the episode id in question
#conn: the connection to use for the database query, if none provided a default is created
def getByEpisodeId(episodeId, conn = None):
	if conn == None:
		conn = mySql.createConnection()
	cursor = conn.cursor()

	cursor.execute("SELECT * FROM Episodes WHERE id = %s", (episodeId))
	if cursor.rowcount == 0:
		return None
	else:
		episodeInfo = cursor.fetchall()[0]
		episodeResult = createFromArray(episodeInfo)
		return episodeResult

#Returns a tv episode that has the given media file id
#mediaFileId: the media file id in question
#conn: the connection to use for the database query, if none provided a default is created
def getByMediaFileId(mediaFileId, conn = None):
	if conn == None:
		conn = mySql.createConnection()
	cursor = conn.cursor()

	cursor.execute("SELECT * FROM Episodes WHERE FK_MediaFile_id = %s", (mediaFileId))
	if cursor.rowcount == 0:
		return None
	else:
		episodeInfo = cursor.fetchall()[0]
		episodeResult = createFromArray(episodeInfo)
		return episodeResult

#Create and return a new tv episode from an array formated by the database
#episodeInfoArray: an array formated as a database return containing tv episode details
def createFromArray(episodeInfoArray):
	episodeResult = episode()
	episodeResult.id = episodeInfoArray[0]
	episodeResult.season = episodeInfoArray[1]
	episodeResult.episode = episodeInfoArray[2]
	episodeResult.associatedSeriesAliasId = episodeInfoArray[3]
	episodeResult.associatedMediaFileId = episodeInfoArray[4]
	return episodeResult

#Create and return a new tv episode
#seasonNumber: the episode season
#episodeNumber: the episode number
def create(seasonNumber, episodeNumber):
	episodeResult = episode()
	episodeResult.season = seasonNumber;
	episodeResult.episode = episodeNumber
	return episodeResult