# based on
# opencv tutorial --> https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_core/py_image_arithmetics/py_image_arithmetics.html

# todo:
# "image stabilisation" = zoom/pan/rotate similar images so they fit together 
# slowly pan panoramic images across screen 
# img1/img2/oddEven --> imgNew/imgOld
# do not enlarge small pictures 
# display information (height/width, date, filename,...) --> not so easy 
# graphical menu 
# play videos 
# react to mouse interaction
# invent some more fancy transitions
# change fade and duration at runtime
# make video-codec selectable by parameter
# try TAPI / OCL https://learnopencv.com/opencv-transparent-api/
# change parameters at runtime 
# on start, grab screen as first image and do some interesting transitions 
# sort images by date, aspect ratio,...
# print compile date, write date tothe \"done\"s
# when freezing picture, allow to move back and forth 
# mask with a growing circle --> better for change between landscape and portrait? 

# done: 
# subdirectries
# limit depth of subdirs
# stop "3rd picture" while blending = freeze
# copy image path+name to clipboard
# loop: do not read and discard the directory every time 
# opencv cannot read a filename containing funny characters 
# option: manually input height and width 
# error handling ... AttributeError: 'NoneType' object has no attribute 'shape'
# Error when blendig images with different color depths (ignore images with color depth other than 3)
# take only newest files. Paramater -a --age: age in days, -1 (default): all files
# convert to grayscale
# blend function completely rewritten --> better timing
# record slideshow as video (still experimental)
# "c" (copy file location) does not work corretly when moving backwards --> OK
# mask inverted
# first and last transition must be a fade
# syntax for masking effects, random effects
# transition masked: on some images, parts of old image remain --> workaround
# change background color when padding images
# hide mouse cursor --> not so easy --> workaround 
# fade time = 0 --> does not switch automatically .... why? --> works now. (Don't know why)
# function keys, cursor keys 
# 2021-05-15 light curve(s)
# 2021-05-17 save picture
# 2021-05-17 scripting 
# 2021-05-17 parameter "mask" renamed to "match"
# 2021-05-17 new parameter "notmatch"
# 2021-05-?? parameters --Match and --Nomatch (case sensitive)
# 2021-05-22 parameter --verbose
# 2021-05-22 bugfix for pause (pressing space/backspace does not terminate pause)
# 2021-05-22 on starup, print pwd and parameters

import numpy as np
import cv2 as cv
import time
import os
import argparse
import re
import random
import clipboard
import pyautogui # for hiding cursor
import math # for sinus in light curve
import sys  # for printing arguments

#----------------------------------------------------------------
# https://forum.opencv.org/t/filename-contains-character/3045/3
def imread_funny (filename):
	'''workaround because cv.imread() cannot handle non-ascii characters (funny characters)'''
	success = True
	image = None
	filename = filename.strip() # trailing newline causes a problem

	try: 
		f = open(filename, "rb")
		b = f.read()
		f.close()
		b = np.frombuffer(b, dtype=np.int8)
		image = cv.imdecode(b, cv.IMREAD_COLOR);
	except Exception as e:
		print ('>>>', e)
		success = False
	
	return (image, success)

#----------------------------------------------------------------
def writeFileInfo (image, filename):
	'''not yet used'''
	text = "filename: " + filename + '\n'
	text = text + "date: " + '\n'
	
	cv.putText (image, text, (20,20))

#----------------------------------------------------------------
# https://thispointer.com/python-how-to-get-list-of-files-in-directory-and-sub-directories/

'''
	For the given path, get the List of all files in the directory tree 
'''
def getListOfFiles(dirName, depth):
	# create a list of file and sub directories 
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
def scaleImage (openName, screenWidth, screenHeight, padColor, convertToGray):
	'''bring an image to the desired height and width, padding it to adjust for aspect ratio'''
	c = 3 # workaround 
	
	# tempImg = cv.imread(openName)
	(tempImg, success) = imread_funny(openName)
	
	if (success):
		try:
			(h,w,c) = tempImg.shape
		except Exception as e:
			print (">>>> ERROR ", openName, ": ", e)
			success = False
	
	if (success):
		if (w>h):
			pl = "l"
		if (h>=w):
			pl = "p"
		if (not pl in args.portrait_landscape):
			success = False
			
	if (success):
		aspectRatioImage = (w+1) / (h+1) 
		aspectRatioScreen = screenWidth / screenHeight
		
		if (aspectRatioImage > aspectRatioScreen):
			newHeight = int(w / aspectRatioScreen)
			newWidth = w
		else:
			newWidth = int(h * aspectRatioScreen)
			newHeight = h
			
		# print ("newWidth: ", newWidth, " newHeight:", newHeight)
		
		topBottom = int((newHeight - h) / 2)
		leftRight = int((newWidth  - w)  / 2)
		color = [0, 0, 0]

		tempImg = cv.copyMakeBorder(tempImg, topBottom, topBottom, leftRight, leftRight, cv.BORDER_CONSTANT, value=padColor)
		
		tempImg = cv.resize(tempImg, (screenWidth, screenHeight), cv.INTER_AREA)
	# else:
		# print (">>>> ERROR Unable to open ", openName)
	
	if (c != 3):
		success = False
		print (">>>> ERROR ", openName, " has color depth of ", c)
	
	# if (args.gray != 0):
	if (convertToGray != 0):
		tempImg = cv.cvtColor(tempImg, cv.COLOR_BGR2GRAY)
		tempImg = cv.cvtColor(tempImg, cv.COLOR_GRAY2BGR) # convert back because we still need a color depth of 3 
	
	return (tempImg, success)
#----------------------------------------------------------------
def addXor(img1,bright1,img2,bright2,oddEven):
	
	if ( oddEven):
		imgA = img2
		imgB = img1
		brightA = bright2
		brightB = bright1
	else:
		imgA = img1
		imgB = img2
		brightA = bright1
		brightB = bright2
	
	if (args.verbose >= 10):
		print (int(100 * brightB), end = '\r')

	cv.imshow ('imgB',imgB)
	cv.imshow ('imgA',imgA)

	
	if (brightB < brightA):
		temp = cv.subtract (imgB, np.array([200 * brightB * 2.0]))
		res = cv.bitwise_xor (temp,imgA)
		cv.imshow ('B',temp)
		cv.imshow ('A',imgA)
	else:
		temp = cv.subtract (imgA, np.array([200 * brightA * 2.0]))
		res = cv.bitwise_xor (temp,imgB)
		cv.imshow ('B',imgB)
		cv.imshow ('A',temp)
	
	return res

#----------------------------------------------------------------
def addMasked(img1,bright1,img2,bright2,oddEven, inverted, oldNew):
	'''add 2 images by calculating a mask which is derived from one of the images'''
	
	
	if (not oddEven):
		imgA = img2
		imgB = img1
		brightA = bright2
		brightB = bright1
	else:
		imgA = img1
		imgB = img2
		brightA = bright1
		brightB = bright2
	
	if (oldNew):
		gray = cv.cvtColor(imgA, cv.COLOR_BGR2GRAY)
	else:
		gray = cv.cvtColor(imgB, cv.COLOR_BGR2GRAY)

	
	if (inverted):
		ret,mask = cv.threshold(gray,255 - int(255 * brightB) + 1,255,cv.THRESH_BINARY)
		mask = cv.bitwise_not (mask)
	else:
		ret,mask = cv.threshold(gray,int(255 * brightB) + 1,255,cv.THRESH_BINARY)

	if (ret):
		maskInverted = cv.bitwise_not (mask)
		maskedA = cv.bitwise_and (imgA, imgA, mask=mask)
		maskedB = cv.bitwise_and (imgB, imgB, mask=maskInverted)
		res = cv.bitwise_or (maskedA, maskedB)
		# cv.imshow ('debug', maskedA)
	else:
		res = cv.addWeighted(img1,bright1,img2,bright2,0)
	
	return res
#----------------------------------------------------------------
def sinusFunc (x, percent):
	y1 = percent / 100 * ((math.sin((x - 0.5) * math.pi) * 1 + 1))
	y2 = (100 - percent)  * x
	y = (y1 + y2) / 2
	return y
	
#----------------------------------------------------------------
def savePic (imgToWrite):
	found = False
	count = 0
	
	pathToWrite = args.path
	testPath = os.path.join (args.path, 'blendPics')
	if os.path.exists (testPath):
		if (os.path.isdir(testPath)):
			pathToWrite = testPath
	
	while (not found):
		filenameToWrite = 'blendPics' + str (count) + '.jpg'
		filenameToWrite = os.path.join (pathToWrite, filenameToWrite)
		if (os.path.exists(filenameToWrite)):
			count = count + 1
		else:
			found = True
	
	if (args.verbose >= 1):
		print ("writing image to ", filenameToWrite)
	cv.imwrite (filenameToWrite, imgToWrite)
		
#----------------------------------------------------------------
def evalKey (key):
	global convertToGray
	global durationTime
	global fadeTime
	global transDict
	
	if (key > 0):
		if (key == ord('g')):
			convertToGray = abs(convertToGray - 1)
			if (args.verbose >= 1):
				print ("convertToGray:", convertToGray)
			key = -1
		elif (key == KEY_F2):
			durationTime = durationTime / 1.5
			if (args.verbose >= 1):
				print ("duration: ", "%.2f" % durationTime, end='\r')
		elif (key == KEY_F3):
			if (durationTime < 0.1):
				durationTime = 0.5
			else:
				durationTime = durationTime * 1.5
			if (args.verbose >= 1):
				print ("duration: ", "%.2f" % durationTime, end='\r')
		elif (key == KEY_F4):
			fadeTime = fadeTime / 1.5
			if (args.verbose >= 1):
				print ("fade: ", "%.2f" % fadeTime, end='\r' )
		elif (key == KEY_F5):
			if (fadeTime < 0.1):
				fadeTime = 0.5
			else:
				fadeTime = fadeTime * 1.5
			if (args.verbose >= 1):
				print ("fade: ", "%.2f" % fadeTime, end='\r' )
		elif (key < 128 and chr(key) in 'bondl'):           # < 128 : avoid error when pressing function/cursor keys
			transDict = setTransitions (chr(key), transDict)
			if (args.verbose >= 1):
				print ("Transitions: ", listTransitions(transDict), end='\r')
			# print (chr(key), transDict) # debug
		else:
			return key
	
	return -1

#----------------------------------------------------------------

def blend (img1, img2, oddEven, fadeTime, duration, transition):
		'''do the actual transition from one image to the other and evaluate users keypresses'''
		global transDict
		global rawTransDict
		global pause


		if (transition == ""):
			possible = []
			if (transDict['b']): 
				possible.append ({'b': 1,'o': 0,'n': 0,'d': 0,'l': 0,'x': 0})
			if (transDict['x']): 
				possible.append ({'b': 0,'o': 0,'n': 0,'d': 0,'l': 0,'x': 1})
			if (transDict['o']): 
				if (transDict['d']):
					possible.append ({'b': 0,'o': 1,'n': 0,'d': 1,'l': 0,'x': 0})
				if (transDict['l']):
					possible.append ({'b': 0,'o': 1,'n': 0,'d': 0,'l': 1,'x': 0})
			if (transDict['n']): 
				if (transDict['d']):
					possible.append ({'b': 0,'o': 0,'n': 1,'d': 1,'l': 0,'x': 0})
				if (transDict['l']):
					possible.append ({'b': 0,'o': 0,'n': 1,'d': 0,'l': 1,'x': 0})
			
			# if nothing is possible, we do a fade
			if (len (possible) == 0):
				possible.append ({'b': 1,'o': 0,'n': 0,'d': 0,'l': 0,'x': 0})

			numPossible = len (possible)
			transIndex = random.randrange(0, numPossible)
			tempTransDict = possible[transIndex]

		else:
			tempTransDict =  setTransitions(transition, rawTransDict)
			
				
		if (args.verbose >= 2):
			print ("*t|" + listTransitions(tempTransDict))
		
		# print (tempTransDict)
		
		timeNextFrame = time.time() + videoInterval
		
		if oddEven:
			bright1 = 1
			bright2 = 0
		else:
			bright1 = 0
			bright2 = 1


		
		dst = img1

		quit = False
		freeze = False
		key = -1
		timeStart = time.time()
		timeEnd = timeStart + fadeTime
		timeBefore = 0
		timeAfter = 0
		key = -1
		
		while (time.time() < timeEnd):
			
			if (freeze):
				timeStart = time.time() - timeBefore
				timeEnd   = time.time() + timeAfter
			else:
				bright = (time.time() - timeStart) / (timeEnd - timeStart)
				# bright = sinusFunc (bright, 100)
				if oddEven:
					bright1 = 1 - bright
					bright2 = bright
				else:
					bright2 = 1 - bright
					bright1 = bright
			

			if (tempTransDict['b']):
				dst = cv.addWeighted(img1,bright1,img2,bright2,0)
			elif (tempTransDict['x']):
				dst = addXor(img1,bright1,img2,bright2,oddEven)
			else:
				dst = addMasked(img1,bright1,img2,bright2,oddEven,tempTransDict['l'],tempTransDict['o'])
			
			cv.imshow('dst',dst)
			if ((args.output != '') and (time.time() > timeNextFrame)):
				out.write(dst)
				timeNextFrame = timeNextFrame + videoInterval

			tempKey = cv.waitKeyEx(1) 
			if (tempKey != -1):
				key = tempKey
				
				if (tempKey == ord ('f')):
					freeze = not freeze
					if (args.verbose >= 1):
						print ('frozen ',freeze, '   ',end = '\r') # +++ python3 only 
					if (freeze):
						timeBefore = time.time() - timeStart
						timeAfter = timeEnd - time.time()
				elif ((tempKey == KEY_UP) or (tempKey == KEY_DOWN)):
					if (freeze):
						if (tempKey == KEY_UP):
							timeBefore = timeBefore + fadeTime / 10
							timeAfter  = timeAfter + fadeTime / 10
						else:
							timeBefore = timeBefore - fadeTime / 10
							timeAfter  = timeAfter - fadeTime / 10
					tempKey = -1
				elif (tempKey < 128 and chr(tempKey) in 'bondl'):
					transDict = setTransitions (chr(tempKey), transDict)
					if (args.verbose >= 1):
						print ("Transitions: ", listTransitions(transDict))
					# print (chr(tempKey), transDict) # debug
					tempKey = -1
				elif (tempKey == ord('s')):
					savePic (dst)
					tempKey = -1
				else:
					key = evalKey(tempKey)
					
					
		
		# blending finished
		
		#workaround for some pictures/transitions when parts of the old image remain
		if (oddEven):
			# cv.imshow ('dst',img2)
			dst = img2
		else:
			dst = img1
			# cv.imshow ('dst',img1)
		cv.imshow ('dst',dst)
		
		# if ((key == 27) or (key == ord('q')) or (key == ord(' ')) or (key == 8)):
		if (key in (27,ord('q'),32,8,KEY_LEFT,KEY_RIGHT)):
			quit = True

		timeThen = time.time() + duration
		while (pause or (time.time() < timeThen) or (duration < 0)) and (not quit):

			if ((args.output != '') and (time.time() > timeNextFrame)):
				out.write(dst)
				timeNextFrame = timeNextFrame + videoInterval
			
			tempKey = cv.waitKeyEx(1)
			
			tempKey = evalKey (tempKey)
			
			if (tempKey == ord('p')):
				pause = not pause
				if (args.verbose >= 1):
					print ('pause ',pause, '   ', end = '\r') # +++ python3 only 
			elif (tempKey != -1):
				key = tempKey
				if ((key == ord(' ')) or (key == 8) or (key == KEY_LEFT) or (key == KEY_RIGHT)):
					break
				if ((key == 27) or (key == ord('q'))):
					quit = True
		# print ("key:", key)
		return (key)

#----------------------------------------------------------------
def setTransitions (transitionsDef, oldDict):
	'''read a string like bondl and switch entries in transitionsDef according to the letters in the string'''
	# global transDict
	newDict = oldDict.copy()
	
	for character in transitionsDef:
		newDict[character] = not newDict[character]
	
	return (newDict)

#----------------------------------------------------------------
def listTransitions (dict):
	'''create a string to output the transitions available'''
	
	res = ''
	keys = dict.keys()
	
	for key in keys:
		if (dict[key]):
			res = res + key
			
	return res

#----------------------------------------------------------------
def maskingAllowed (dict):
	'''see if we are allowed to use masking'''
	
	return (dict['o'] or dict['n']) and (dict['d'] or dict['l'])
#----------------------------------------------------------------
def readBgColor (inString):
	'''read a string like #aabbcc and convert it to BGR-value (not RGB!)'''
	if (inString[0] != '#') or (len(inString) != 7):
		return ([0,0,0])
	
	inString = inString[1:7]
	
	res = []
	
	# for countDoubles in range (3):
	for countDoubles in range (2,-1,-1):
		hex = 0
		substr = inString[2 * countDoubles : 2 * countDoubles + 2]
		# print (substr)
		hex = int (substr, 16)
		# print ('dez:',hex)
		res.append (hex)
		
	return res
#----------------------------------------------------------------
def bubbleShuffle (array, randomPercent):
	# randomPercent < 0 ... do nothing
	if (randomPercent < 0):
		return
	
	# randomPercent 100% ... normal shuffle
	if (randomPercent >= 100):
		random.shuffle(array)
		return
	
	array.sort()
	
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

#----------------------------------------------------------------
parser = argparse.ArgumentParser(description = "display all images in folder with nice transitions", epilog = "Esc/q=quit, p=pause on/off, f=freeze on/off, s(while blending)=save picture, c=copy filename to clipboard, b/o/n/d/l=change transition, left arrow or backspace=previous, right arrow or space=next, F2,F3,F4,F5=decrease/increase fade-time/duration" )
parser.add_argument("-p", "--path", type=str, default=".", help="path where images are found")
parser.add_argument("-s", "--subdirs", type=int, default=0, help="depth of subdirectories.  0 (default): no subdirs, -1: all subdirs")
parser.add_argument("-d", "--duration", type=float, default="5", help="time image is shown [seconds]. -1 for manual switching")
parser.add_argument("-f", "--fade", type=float, default="1.5", help="time of fading effect [seconds]")
parser.add_argument("-t", "--transition", type=str, default="bondl", help="types of transition. Combination of the letters b,o,n,d,l")
parser.add_argument("-m", "--match", type=str, default=".", help="mask filename (regex syntax, case insensitive)")
parser.add_argument("-M", "--Match", type=str, default=".", help="mask filename (regex syntax, case sensitive)")
parser.add_argument("-n", "--notmatch", type=str, default="", help="negative mask filename (regex syntax, case insensitive)")
parser.add_argument("-N", "--NotMatch", type=str, default="", help="negative mask filename (regex syntax, case sensitive)")
parser.add_argument("-pl", "--portrait_landscape", type=str, default="pl", help="filter portrait or landscape. p = portrait, l = landscape, pl (default) = both")
parser.add_argument("-l", "--loop", type=int, default="1", help="nr. of loops, -1 = loop forever, default=1")
parser.add_argument("-a", "--age",  type=float, default="-1.0", help="maximal age of file in days. -1.0 (default): all files")
parser.add_argument("-g", "--gray", type=int, default="0", help="0 (default): color, all else: convert to grayscale")
parser.add_argument("-r", "--random", type=int, default="-1", help="random shuffle. -1 (default): leave as is, 0: sorted, 0..100: shuffle")
parser.add_argument("-i", "--input", type=str, default="", help="input file, containing filenames and parameters (script)")
parser.add_argument("-v", "--verbose", type=int, default="1", help="verbose ... 0=only errors, 1=print filenames, 1=print all data")
parser.add_argument("-o", "--output", type=str, default="", help="output video file (very experimental)")
parser.add_argument("-w", "--width", type=int, default="-1", help="width. -1 (default): automatic")
parser.add_argument("-hh", "--height", type=int, default="-1", help="height. -1 (default): automatic")
parser.add_argument("--fps", type=float, default=30, help="fps of output video (very experimental)")
parser.add_argument("-bg", "--background", type=str, default="#000000", help="background color in hex values (rgb) like #aabbcc")

args = parser.parse_args()

KEY_UP   = 0x260000
KEY_DOWN = 0x280000
KEY_LEFT = 0x250000
KEY_RIGHT= 0x270000
KEY_F1   = 0x700000
KEY_F2   = 0x710000
KEY_F3   = 0x720000
KEY_F4   = 0x730000
KEY_F5   = 0x740000
KEY_F6   = 0x750000
KEY_F7   = 0x760000
KEY_F8   = 0x770000
KEY_F9   = 0x780000
KEY_F11  = 0x790000
KEY_F12  = 0x7a0000
KEY_F1   = 0x7b0000
KEY_PGUP = 0x210000
KEY_PGDN = 0x220000
KEY_HOME = 0x240000
KEY_END  = 0x230000


extensionsPhoto = ('.png', '.jpg', '.jpeg', '.jfif', '.tiff', '.bmp' , '.webp', '.gif') 
key = 0
pause = False

if (args.verbose >= 1):
	print ("blendPics by Martin Piehslinger")
	print ("*******************************")
	print ("")
	print ('current working directory: ', os.getcwd(), ', command line parameters:', sys.argv)
# try:
	# import builddate
	# print ("Version from ", builddateString)
# except ImportError:
	# pass


rawTransDict = {
	'b': False,			# fade --> blend
	'o': False,		# maskOld
	'n': False,		#maskNew
	'd': False,	# dark
	'l': False,	# light
	'x': False	# xor
}

if (args.transition == "fade"):
	transitionString = "b"
elif (args.transition == "mask"):
	transitionString = "ol"
elif (args.transition == "imask"):
	transitionString = "od"
else: 
	transitionString = args.transition
transDict = setTransitions(transitionString, rawTransDict)

if (args.verbose >= 1):
	print ("Transitions: ", listTransitions(transDict))

if maskingAllowed (transDict):
	blendString = 'nd'
else:
	blendString = 'b'

fadeTime = args.fade
durationTime = args.duration
convertToGray = args.gray


if (args.output != ''):
	fourcc = cv.VideoWriter_fourcc(*'XVID')
	out = cv.VideoWriter(args.output, fourcc, args.fps, (w+1,  h+1))
videoInterval = 1 / args.fps



if (args.input == ''):
	if (args.verbose >= 1):
		print ("searching images...")
	fileList = getListOfFiles(args.path, args.subdirs)

	filenames = []
	for filename in fileList:
		addFile = True
		if (filename.lower().endswith(extensionsPhoto)):
			if (not re.search(args.match,filename,flags=re.IGNORECASE)):
				addFile = False
			if (not re.search(args.Match,filename)):
				addFile = False
			if (args.notmatch != '' and re.search(args.notmatch,filename,flags=re.IGNORECASE)):
				addFile = False
			if (args.NotMatch != '' and re.search(args.NotMatch,filename)):
				addFile = False
			if (args.age > 0):
				age = time.time() - os.path.getmtime(filename) 
				age = age / 3600 / 24 # age in days
				# print ("age: ",age," max age:" , args.age, addFile, age > args.age)
				if (age > args.age):
					addFile = False
			if (addFile):
				filenames.append (filename)
			
			# trying some more sophisticated evaluation, especially when doing a negative lookahead assertion
			# does not work....
			# result = re.search(args.match,filename)
			# if (result):
				# (start,end) = result.span()
				# print (start,end,filename)
				# if (end > start):
					# filenames.append (os.path.join(args.path, filename))


		
	# if (args.random == 0):
		# print ("sorting...")
		# filenames.sort()
		
	# print (filenames)
else:
	try:
		inputList = open (args.input,'r')
	except Exception as e:
		print (e)
		exit()
	filenames = inputList.readlines()
	inputList.close()

NumFiles = len(filenames)
if (args.verbose >= 1):
	print (NumFiles, "files found", " total duration approx", int (NumFiles * (fadeTime + durationTime) / 60), " minutes")
if (NumFiles == 0):
	exit()

if ((args.width > 0) and (args.height > 0)):
	flag = cv.WND_PROP_AUTOSIZE
	mode = cv.WINDOW_AUTOSIZE
	w = args.width
	h = args.height
else:
	flag = cv.WND_PROP_FULLSCREEN
	mode = cv.WINDOW_FULLSCREEN
	w = -1
	h = -1
	


# Window in full-screen-mode, determine aspect ratio of screen
cv.namedWindow("dst", flag)
cv.setWindowProperty("dst",flag,mode)
if ((w < 0) or (h < 0)):
	(a,b,w,h) = cv.getWindowImageRect('dst')
aspectRatioScreen =  (w+1) / (h+1)
if (args.verbose >= 1):
	print ('Screen: ', w+1, h+1, "%.2f" % aspectRatioScreen)


bgColor = readBgColor(args.background)

black = np.zeros((h+1, w+1, 3), np.uint8)
black[:] = bgColor
img1 = black
img2 = black
cv.imshow('dst',black)
cv.waitKey(1000)

oddEven = True
FirstTime = True

pyautogui.FAILSAFE = False
pyautogui.moveTo(0,0) # to hide the mouse cursor

loopCount = 0

while ((loopCount < args.loop) or (args.loop == -1)):

	bubbleShuffle (filenames, args.random)
	
	# if (args.random != 0):
		# print ("shuffle....")
		# random.shuffle (filenames) 


	IndexFiles = 0
	running = True
	Back = False

	while ((IndexFiles >= 0) and (IndexFiles < NumFiles) and running):
		
		if (filenames[IndexFiles].startswith('*')):
			commands = filenames[IndexFiles].split ('*')
			for command in commands:
				if (len(command) > 0):
					# print (command)
					(key,val) = command.split ('|')
					if (key == 'n'):
						imgName = val
					elif (key == 'f'):
						fadeTime = float(val)
					elif (key == 'd'):
						durationTime = float(val)
					elif (key == 't'):
						transitionString = val
						
		else:
			imgName = filenames[IndexFiles]
		
		if (args.verbose >= 2):
			print ('*n|' + imgName + '*d|' + "%.2f" % durationTime + '*f|' + "%.2f" % fadeTime,end = '')
		elif (args.verbose >= 1):
			print (imgName)
		if oddEven:
			(img2, success) = scaleImage(imgName, w+1, h+1, bgColor, convertToGray)
		else:
			(img1, success) = scaleImage(imgName, w+1, h+1, bgColor, convertToGray)
		
		# Back = False
		
		if (success):
			if (FirstTime):
				key = blend (img1, img2, oddEven, fadeTime, durationTime, blendString) #{'b': 0,'o': 0,'n': 1,'d': 1,'l': 0})
			else:
				key = blend (img1, img2, oddEven, fadeTime, durationTime, '')
			FirstTime = False
			Back = False
			if (key > 0):
				# print (chr(key))
				if ((key == ord('q')) or (key == 27)):
					if (args.verbose >= 1):
						print ("interrupted by user")
					running = False

				elif ((key == 8) or (key == KEY_LEFT)):
					Back = True
					key = -1
				elif (key == ord('c')):
					if (args.verbose >= 1):
						print ("copying ", imgName, " to clipboard")
					clipboard.copy (imgName)
					key = -1
			
			oddEven = not oddEven
		else:
			print ("Skipped ", imgName)
			
			
		if (Back):
			IndexFiles = IndexFiles - 1
		else:
			IndexFiles = IndexFiles + 1


	loopCount = loopCount + 1

	if ((key == ord('q')) or (key == 27)):
		if (args.verbose >= 1):
			print ("break")
		break
		
# done, fade out
if (oddEven):
	img2 = black
else:
	img1 = black
	
if maskingAllowed (transDict):
	blendString = 'od'
else:
	blendString = 'b'


blend (img1, img2, oddEven, fadeTime, 0, blendString ) # {'b': 0,'o': 1,'n': 0,'d': 1,'l': 0})
cv.waitKey (1000)

if (args.verbose >= 1):
	print ("Done.")
cv.destroyAllWindows()
if (args.output != ''):
	out.release()