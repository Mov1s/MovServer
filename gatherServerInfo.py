import os
import commonSettings

def main():
	systemConf = commonSettings.systemSettings()
	webDir = os.path.join(systemConf.wwwDirectory, 'movServer')
	infoFile = os.path.join(webDir, 'info.txt')

	os.system('(echo -n "Free space: "; df -h | grep sdb | awk "{ print $4 }") > ' + infoFile)
	os.system('(echo -n "Percentage used: "; df -h | grep sdb | awk "{ print $5 }") >> ' + infoFile)
	os.system('(echo -n "Movie count: "; ls -1R /srv/local/sdb/Content/Movies | wc -l) >> ' + infoFile)
	os.system('(echo -n "Episode count: "; ls -1R /srv/local/sdb/Content/TV | wc -l) >> ' + infoFile)
	os.system('(echo -n "Free space: "; df -h | grep sdc | awk "{ print $4 }") >> ' + infoFile)
	os.system('(echo -n "Percentage used: "; df -h | grep sdc | awk "{ print $5 }") >> ' + infoFile)
	os.system('(echo -n "Movie count: "; ls -1R /srv/local/sdc/Content/Movies | wc -l) >> ' + infoFile)
	os.system('(echo -n "Episode count: "; ls -1R /srv/local/sdc/Content/TV | wc -l) >> ' + infoFile)
