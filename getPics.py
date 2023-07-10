
import os
import random

import numpy as np
import cv2
import sys

import exifRoutines


#---------------------------------------------------------------
def meanVal (pic):

	try: 
		img = cv2.imread(pic)
		img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	except Exception:
		return 0
	h,s,v = cv2.split(img_hsv)
	# bright_pixel = np.amax(v)
	# print(bright_pixel)
	# bright_pixel will give max illumination value in the image

	mean_val = np.mean (v)
	print ("mean_val", mean_val)
	return mean_val
#---------------------------------------------------------------
def meanSat (pic):

	try: 
		img = cv2.imread(pic)
		img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	except Exception:
		return 0
	h,s,v = cv2.split(img_hsv)
	# bright_pixel = np.amax(v)
	# print(bright_pixel)
	# bright_pixel will give max illumination value in the image

	mean_sat = np.mean (s)
	print ("mean_sat", mean_sat)
	return mean_sat

#---------------------------------------------------------------
def meanHue (pic):

	try: 
		img = cv2.imread(pic)
		img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	except Exception:
		return 0
	h,s,v = cv2.split(img_hsv)
	# bright_pixel = np.amax(v)
	# print(bright_pixel)
	# bright_pixel will give max illumination value in the image

	mean_hue = np.mean (h)
	print ("mean_hue", mean_hue)
	return mean_hue

#--------------------------------------------------------------
def getAspectRatio (pic):
	try: 
		img = cv2.imread(pic)
		(h,w,c) = img.shape
	except Exception:
		return 1
	aspect = w / h
	return aspect

#--------------------------------------------------------------
def getSize (pic):
	try: 
		img = cv2.imread(pic)
		(h,w,c) = img.shape
	except Exception:
		return 1
	size = w * h
	return size

#--------------------------------------------------------------
def getOsDir (pic):
	pic = pic.lower()
	(head,tail) = os.path.split(pic)
	return head
#--------------------------------------------------------------
def getOsFile (pic):
	pic = pic.lower()
	(head,tail) = os.path.split(pic)
	return tail
#----------------------------------------------------------------
# https://thispointer.com/python-how-to-get-list-of-files-in-directory-and-sub-directories/

'''
	For the given path, get the List of all files in the directory tree 
'''
def getListOfFiles(dirName, depth):
	# create a list of files and sub directories 
	# names in the given directory 
	try:
		listOfFile = os.listdir(dirName)
	except Exception as e:
		return list()
	allFiles = list()
	# Iterate over all the entries
	for entry in listOfFile:
		# Create full path
		fullPath = os.path.join(dirName, entry)
		# If entry is a directory then get the list of files in this directory 
		if (os.path.isdir(fullPath)):
			if (depth != 0):
				allFiles = allFiles + getListOfFiles(fullPath, depth-1)
		else:
			allFiles.append(fullPath)
				
	return allFiles

#----------------------------------------------------------------
def bubbleShuffle (arrayAll, randomPercent, probability, sortParameter):
	# global welcome
	
	array = []
	for file in arrayAll:
		if (random.randrange(0, 100) < probability):
			array.append(file)
	
	# array.sort()
	# array.sort(key = lambda x: exifRoutines.getImageTime(x)) ### +++ commandline-parameter berücksichtigen 
	
	# sortString = "exifRoutines.getImageTime(x)"
	# sortString = "os.path.getmtime(x)"
	# sortString = "x"
	sortString = ""
	
	# if sortParameter != "":
		# writeToPic (welcome, "sorting...", -1)
	
	sortMethods = sortParameter.split (";")
	for sortMethod in sortMethods:
		sortString = ""
		if sortMethod != "":
			
			sortOptions = sortMethod.split (":")
			if sortOptions[0] == "exif":
				sortString = "exifRoutines"
				if len (sortOptions) >= 2:
					if sortOptions[1] == "time":
						sortString = sortString + ".getImageTime(x)"
					else: 
						sortString = sortString + "." + "geExifString(x, \"" + sortOptions[1] + "\")" # if anything else is specified, pass it directly to geExifString
			elif sortOptions[0] == "os":
				sortString = "os"
				if len (sortOptions) >= 2:
					if sortOptions[1] == "time":
						sortString = sortString + ".path.getmtime(x)"
					elif sortOptions[1] == "dir":
						sortString = "getOsDir(x)"
					elif sortOptions[1] == "file":
						sortString = "getOsFile(x)"
			elif sortOptions[0] == "name":
				sortString = "x"
			elif sortOptions[0] == "pic":
				if len (sortOptions) >= 2:
					if sortOptions[1] == "hue":
						sortString = sortString + "meanHue(x)"
					elif sortOptions[1] == "sat":
						sortString = sortString + "meanSat(x)"
					elif sortOptions[1] == "val":
						sortString = sortString + "meanVal(x)"
					elif sortOptions[1] == "asp":
						sortString = sortString + "getAspectRatio(x)"
					elif sortOptions[1] == "size":
						sortString = sortString + "getSize(x)"
			else: 
				sortString = sortMethod # if anything else is specified, pass it directly to the sort routine
			
			if sortOptions[ -1] == "down": # up | down
				reverse = True
			else:
				reverse = False
			
			# logMessage (2, "sort key = " + sortString)
			array.sort(key = lambda x: eval(sortString), reverse = reverse) 
	
	# array.sort(key= lambda x : exifRoutines.getImageTime(x))  ###+++ workaround, immer exif time verwenden
	# logMessage (1, "# done sorting....")
	
	# randomPercent < 0 ... do nothing
	if (randomPercent <= 0):
		return array
	
	# randomPercent 100% ... normal shuffle
	if (randomPercent >= 100):
		random.shuffle(array)
		return array
	
	Len = len(array)
	window = int (Len * randomPercent / 100)
	if (window < 2):
		window = 2
	# print ("window", window)
	
	winStep =  int(window / 2) 
	if (winStep == 0):
		winStep = 1
	
	# for winStart in range (0, Len - window, winStep):
	for winStart in range (0, Len, winStep):		# one too many, but so we are sure to shuffle up to the end
		winEnd = winStart+window
		if (winEnd > Len):
			winEnd = Len
		# print ("sorting from ", winStart, " to ", winEnd)
		subset = array[winStart:winEnd]
		random.shuffle  (subset)
		array[winStart:winEnd] = subset
	
	return array
