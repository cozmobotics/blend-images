import time

def builddate():
	now = time.localtime()
	builddate = time.strftime('%Y-%m-%d %H:%M', now)
	return builddate
	
f = open ('builddate.py', 'w')
f.write ('builddateString = \"' + builddate() + '\"')
f.close