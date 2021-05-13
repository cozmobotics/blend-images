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
# light curve(s)
# scripting 
# change parameters at runtime 
# on start, grab screen as first image and do some interesting transitions 

# done: 
# subdirectries
# limit depth of subdirs
# stop "3rd picture" while blending = freeze
# copy image path+name to clipboard
# loop: do not read and discard the directory every time 
# opencv cannot read a filename containing funny characters like » 
# option: manually input height and width 
# error handling ... AttributeError: 'NoneType' object has no attribute 'shape'
# Error when blendig images with different color depths (ignore images with color depth other than 3)
# take only newest files. Paramater -a --age: age in days, -1 (default): all files
# convert to grayscale
# blend function completely rewritten --> better timing
# record slideshow as video (still experimental)
# "c" (copy file location) does not work corretly when moving backwards 
# mask inverted
# first and last transition must be a fade
# syntax for masking effects, random effects
# transition masked: on some images, parts of old image remain --> workaround
# change background color when padding images
# hide mouse cursor --> not so easy --> workaround 
# fade time = 0 --> does not switch automatically .... why? --> works now. (Don't know why)

import numpy as np
import cv2 as cv
import time
import os
import argparse
import re
import random
import clipboard
import pyautogui

#----------------------------------------------------------------
# https://forum.opencv.org/t/filename-contains-character/3045/3
def imread_funny (filename):
	'''workaround because cv.´imread() cannot handle non-ascii characters (funny characters)'''
	success = True
	image = None
	
	try: 
		f = open(filename, "rb")
		b = f.read()
		f.close()
		b = np.frombuffer(b, dtype=np.int8)
		image = cv.imdecode(b, cv.IMREAD_COLOR);
	except Exception as e:
		print (e)
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
	listOfFile = os.listdir(dirName)
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
def scaleImage (openName, screenWidth, screenHeight, padColor):
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
	
	if (args.gray != 0):
		tempImg = cv.cvtColor(tempImg, cv.COLOR_BGR2GRAY)
		tempImg = cv.cvtColor(tempImg, cv.COLOR_GRAY2BGR) # convert back because we still need a color depth of 3 
	
	return (tempImg, success)
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

def blend (img1, img2, oddEven, fadeTime, duration, transition):
		'''do the actual transition from one image to the other and evaluate users keypresses'''
		global transDict
		global rawTransDict


		if (transition == ""):
			possible = []
			if (transDict['b']): 
				possible.append ({'b': 1,'o': 0,'n': 0,'d': 0,'l': 0})
			if (transDict['o']): 
				if (transDict['d']):
					possible.append ({'b': 0,'o': 1,'n': 0,'d': 1,'l': 0})
				if (transDict['l']):
					possible.append ({'b': 0,'o': 1,'n': 0,'d': 0,'l': 1})
			if (transDict['n']): 
				if (transDict['d']):
					possible.append ({'b': 0,'o': 0,'n': 1,'d': 1,'l': 0})
				if (transDict['l']):
					possible.append ({'b': 0,'o': 1,'n': 1,'d': 0,'l': 1})
			
			# if nothing is possible, we do a fade
			if (len (possible) == 0):
				possible.append ({'b': 1,'o': 0,'n': 0,'d': 0,'l': 0})

			numPossible = len (possible)
			transIndex = random.randrange(0, numPossible)
			tempTransDict = possible[transIndex]

		else:
			tempTransDict =  setTransitions(transition, rawTransDict)
			# tempTransDict = {'b': 1,'o': 0,'n': 0,'d': 0,'l': 0}
			# tempTransDict = {'b': 0,'o': 0,'n': 1,'d': 1,'l': 0}
			
				
			
		
		# print (tempTransDict)
		
		timeNextFrame = time.time() + videoInterval
		
		if oddEven:
			bright1 = 1
			bright2 = 0
		else:
			bright1 = 0
			bright2 = 1


		
		# dst = cv.addWeighted(img1,bright1,img2,bright2,0)  # just to initialize variable dst
		dst = img1
		# cv.imshow('dst',dst)

		quit = False
		freeze = False
		pause = False
		key = -1
		timeStart = time.time()
		timeEnd = timeStart + fadeTime
		timeBefore = 0
		timeAfter = 0
		
		while (time.time() < timeEnd):
			
			if (freeze):
				timeStart = time.time() - timeBefore
				timeEnd   = time.time() + timeAfter
			else:
				bright = (time.time() - timeStart) / (timeEnd - timeStart)
				if oddEven:
					bright1 = 1 - bright
					bright2 = bright
				else:
					bright2 = 1 - bright
					bright1 = bright

			if (tempTransDict['b']):
				dst = cv.addWeighted(img1,bright1,img2,bright2,0)
			else:
				dst = addMasked(img1,bright1,img2,bright2,oddEven,tempTransDict['l'],tempTransDict['o'])
			
			cv.imshow('dst',dst)
			if ((args.output != '') and (time.time() > timeNextFrame)):
				out.write(dst)
				timeNextFrame = timeNextFrame + videoInterval

			tempKey = cv.waitKey(1) 
			if (tempKey != -1):
				key = tempKey
				
				if (tempKey == ord ('f')):
					freeze = not freeze
					print ('frozen ',freeze, '   ',end = '\r')
					if (freeze):
						timeBefore = time.time() - timeStart
						timeAfter = timeEnd - time.time()
				elif (chr(tempKey) in 'bondl'):
					transDict = setTransitions (chr(tempKey), transDict)
					print ("Transitions: ", listTransitions(transDict))
					# print (chr(tempKey), transDict) # debug
					tempKey = -1
				else:
					key = tempKey
					
					
		
		# blending finished
		
		#workaround for sime pictures/transitions when parts of the old image remain
		if (oddEven):
			# cv.imshow ('dst',img2)
			dst = img2
		else:
			dst = img1
			# cv.imshow ('dst',img1)
		cv.imshow ('dst',dst)
		
		if ((key == 27) or (key == ord('q')) or (key == ord(' ')) or (key == 8)):
			quit = True

		timeThen = time.time() + duration
		while (pause or (time.time() < timeThen) or (duration < 0)) and (not quit):

			if ((args.output != '') and (time.time() > timeNextFrame)):
				out.write(dst)
				timeNextFrame = timeNextFrame + videoInterval
			
			tempKey = cv.waitKey(1)
			
			if (tempKey != -1):
				if (tempKey == ord('p')):
					pause = not pause
					print ('pause ',pause, '   ', end = '\r')
				elif (chr(tempKey) in 'bondl'):
					transDict = setTransitions (chr(tempKey), transDict)
					print ("Transitions: ", listTransitions(transDict))
					# print (chr(tempKey), transDict) # debug
					tempKey = -1
				else: 
					key = tempKey
					if ((key == ord(' ')) or (key == 8)):
						break
					if ((key == 27) or (key == ord('q'))):
						quit = True
				# if (duration < 0):
					# break
	
			
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
parser = argparse.ArgumentParser(description = "display all images in folder with nice transitions", epilog = "Esc/q=quit, p=pause on/off, f=freeze on/off, c=copy filename to clipboard, b/o/n/d/l=change transition, backspace=previous, space=next")
parser.add_argument("-p", "--path", type=str, default=".", help="path where images are found")
parser.add_argument("-s", "--subdirs", type=int, default=0, help="depth of subdirectories.  0 (default): no subdirs, -1: all subdirs")
parser.add_argument("-d", "--duration", type=float, default="5", help="time image is shown [seconds]. -1 for manual switching")
parser.add_argument("-f", "--fade", type=float, default="1.5", help="time of fading effect [seconds]")
parser.add_argument("-t", "--transition", type=str, default="bondl", help="types of transition. Combination of the letters b,o,n,d,l")
parser.add_argument("-m", "--mask", type=str, default=".", help="mask filename (regex syntax)")
parser.add_argument("-pl", "--portrait_landscape", type=str, default="pl", help="filter portrait or landscape. p = portrait, l = landscape, pl (default) = both")
parser.add_argument("-l", "--loop", type=int, default="1", help="nr. of loops, -1 = loop forever, default=1")
parser.add_argument("-a", "--age",  type=float, default="-1.0", help="maximal age of file in days. -1.0 (default): all files")
parser.add_argument("-g", "--gray", type=int, default="0", help="0 (default): color, all else: convert to grayscale")
parser.add_argument("-r", "--random", type=int, default="0", help="random shuffle. 0 (default): sorted, all else: shuffeled")
parser.add_argument("-w", "--width", type=int, default="-1", help="width. -1 (default): automatic")
parser.add_argument("-hh", "--height", type=int, default="-1", help="height. -1 (default): automatic")
parser.add_argument("-o", "--output", type=str, default="", help="output video file (very experimental)")
parser.add_argument("--fps", type=float, default=30, help="fps of output video (very experimental)")
parser.add_argument("-bg", "--background", type=str, default="#000000", help="background color in hex values (rgb) like #aabbcc")

args = parser.parse_args()

extensionsPhoto = ('.png', '.jpg', '.jpeg', '.jfif', '.tiff', '.bmp' , '.webp', '.gif') 
steps = 50
key = 0


rawTransDict = {
	'b': False,			# fade --> blend
	'o': False,		# maskOld
	'n': False,		#maskNew
	'd': False,	# dark
	'l': False	# light
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
print ("Transitions: ", listTransitions(transDict))

if maskingAllowed (transDict):
	blendString = 'nd'
else:
	blendString = 'b'


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
print ('Screen: ', w+1, h+1, aspectRatioScreen)

if (args.output != ''):
	fourcc = cv.VideoWriter_fourcc(*'XVID')
	out = cv.VideoWriter(args.output, fourcc, args.fps, (w+1,  h+1))
videoInterval = 1 / args.fps


loopCount = 0

print ("searching images...")
# if (args.subdirs != 0):
	# fileList = getListOfFiles(args.path)
# else:
	# fileList = os.listdir(path=args.path)
	
fileList = getListOfFiles(args.path, args.subdirs)

filenames = []
for filename in fileList:
	addFile = True
	if (filename.lower().endswith(extensionsPhoto)):
		if (not re.search(args.mask,filename)):
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
		# result = re.search(args.mask,filename)
		# if (result):
			# (start,end) = result.span()
			# print (start,end,filename)
			# if (end > start):
				# filenames.append (os.path.join(args.path, filename))


NumFiles = len(filenames)
print (NumFiles, "files found")
if (NumFiles == 0):
	exit()
	
if (args.random == 0):
	print ("sorting...")
	filenames.sort()
	
# print (filenames)

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

while ((loopCount < args.loop) or (args.loop == -1)):

	if (args.random != 0):
		print ("shuffle....")
		random.shuffle (filenames) 


	IndexFiles = 0
	running = True
	Back = False

	while ((IndexFiles >= 0) and (IndexFiles < NumFiles) and running):
		
		imgName = filenames[IndexFiles]
		
		print ('\nImage nr. ', IndexFiles, ' ', imgName)
		if oddEven:
			(img2, success) = scaleImage(imgName, w+1, h+1, bgColor)
		else:
			(img1, success) = scaleImage(imgName, w+1, h+1, bgColor)
		
		# Back = False
		
		if (success):
			if (FirstTime):
				key = blend (img1, img2, oddEven, args.fade, args.duration, blendString) #{'b': 0,'o': 0,'n': 1,'d': 1,'l': 0})
			else:
				key = blend (img1, img2, oddEven, args.fade, args.duration, '')
			FirstTime = False
			Back = False
			if (key > 0):
				# print (chr(key))
				if ((key == ord('q')) or (key == 27)):
					print ("interrupted by user")
					running = False

				elif (key == 8):
					Back = True
					key = -1
				elif (key == ord('c')):
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


blend (img1, img2, oddEven, args.fade, 0, blendString ) # {'b': 0,'o': 1,'n': 0,'d': 1,'l': 0})
cv.waitKey (1000)

print ("Done.")
cv.destroyAllWindows()
if (args.output != ''):
	out.release()