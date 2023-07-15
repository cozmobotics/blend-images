import datetime
from exif import Image 
import time
import os

extensionsPhoto = ('.png', '.jpg', '.jpeg', '.jfif', '.tiff', '.bmp' , '.webp', '.gif') 
###+++ besser: mit imgHeader machen, siehe https://www.blog.pythonlibrary.org/2020/02/09/how-to-check-if-a-file-is-a-valid-image-with-python/


#------------------------------------------------------
def getFileTime (filename):
	# return os.path.getmtime(filename)
	return str(os.path.getmtime(filename))

#----------------------------------------------------------------
def getImageTime (filename):
	format = "%Y:%m:%d %H:%M:%S"
	
	if (filename.lower().endswith(extensionsPhoto)):
		dateString = geExifString(filename, "datetime") # datetime waere sowieso default, aber im es klarer zu machen 
	else:
		return os.path.getmtime(filename)
	
	if dateString == "":
		return os.path.getmtime(filename)
	else:
		dt_object = datetime.datetime.strptime(dateString, format)
		unixT = time.mktime(dt_object.timetuple())
		# return unixT
		return str (unixT)

#----------------------------------------------------------------
def geExifString (filename, toFind = "datetime"):
	try:
		ImageRaw = open(filename, 'rb')
	except Exception:
		# return ""
		return getFileTime (filename)
	
	try:
		ImageBin = Image (ImageRaw)
	except Exception:
		# return ""
		return getFileTime (filename)
	
	try:
		# print (ImageBin["datetime"], filename)
		return ImageBin[toFind]
	except Exception:
		# return ""
		return getFileTime (filename)

