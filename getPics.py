'''
Routines for reading, shuffeling and sorting images 

2026-02-17: support for windows .lnk (= link) files
'''
import os
import random

import numpy as np
import cv2
import sys

import exifRoutines

import win32com.client

def get_lnk_target(path):	# 2026-02-17
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(path)
    return shortcut.Targetpath  # plus z.B. shortcut.Arguments bei Bedarf

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
	# print ("mean_val", mean_val)
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
	# print ("mean_sat", mean_sat)
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
	# print ("mean_hue", mean_hue)
	return mean_hue

#---------------------------------------------------------------
def meanHue2 (pic):

	''' mean hue of the image with correction of hue. Looks more natural, but takes long. '''

	try: 
		img = cv2.imread(pic)
		img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	except Exception:
		return 0
	h,s,v = cv2.split(img_hsv)
	
	# correction of hue: 170 looks rather warm
	for row in range (len(h)):
		for col in range (len(h[0])):
			if h[row][col] > 145:
				h[row][col] = 170 - h[row][col]
	
	# bright_pixel = np.amax(v)
	# print(bright_pixel)
	# bright_pixel will give max illumination value in the image

	mean_hue = np.mean (h)
	# print ("mean_hue", mean_hue)
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
	# print ("size: ", size)
	return size

#--------------------------------------------------------------
def getHeight (pic):
	try: 
		img = cv2.imread(pic)
		(h,w,c) = img.shape
	except Exception:
		return 1
	# print ("height: ", h)
	return h

#--------------------------------------------------------------
def getWidth (pic):
	try: 
		img = cv2.imread(pic)
		(h,w,c) = img.shape
	except Exception:
		return 1
	return w

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
#--------------------------------------------------------------
def getOsFullName (pic):
	pic = pic.lower()
	return pic
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
		
		fName,fExt = os.path.splitext(entry)	# 2026-02-17
		if fExt == ".lnk":
			fullPath = get_lnk_target(fullPath)
		
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
					elif sortOptions[1] == "fullname":
						sortString = "getOsFullName(x)"
					else:
						print ("Please select sort option for sort method os: time, dir, file, fullname")
						sys.exit()
			elif sortOptions[0] == "name":
				sortString = "x"
			elif sortOptions[0] == "pic":
				if len (sortOptions) >= 2:
					if sortOptions[1] == "hue":
						sortString = sortString + "meanHue(x)"
					elif sortOptions[1] == "hue2":
						sortString = sortString + "meanHue2(x)" # with correction, but very slow
					elif sortOptions[1] == "sat":
						sortString = sortString + "meanSat(x)"
					elif sortOptions[1] == "val":
						sortString = sortString + "meanVal(x)"
					elif sortOptions[1] == "asp":
						sortString = sortString + "getAspectRatio(x)"
					elif sortOptions[1] == "height":
						sortString = sortString + "getHeight(x)"
					elif sortOptions[1] == "width":
						sortString = sortString + "getWidth(x)"
					elif sortOptions[1] == "size":
						sortString = sortString + "getSize(x)"
					else:
						print ("Please select sort option for sort method pic: hue, sat, val, height, width, size")
						sys.exit()
			else: 
				# sortString = sortMethod # if anything else is specified, pass it directly to the sort routine
				print ("Please select sortMethod = exif, os, name, pic")
				sys.exit()
			
			if sortOptions[ -1] == "down": # up | down
				reverse = True
			else:
				reverse = False
			
			# logMessage (2, "sort key = " + sortString)
			if sortString != 'none':
				# array.sort(key = lambda x: eval(sortString), reverse = reverse) 
				array.sort(key = lambda x: eval(sortString), reverse = reverse) 
				
				# +++++++++++++++++++ debug +++++++++++++++++
				print ("#>>>>>>>>>>>>>>>>>>>>", sortString, "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
				# for x in array:
					# print (eval(sortString))
	
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
