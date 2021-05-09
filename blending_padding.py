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
# hide mouse cursor --> not so easy 
# react to mouse interaction
# invent some fancy transitions
# fade time = 0 --> does not switch automatically .... why?
# change fade and duration at runtime

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

import numpy as np
import cv2 as cv
import time
import os
import argparse
import re
import random
import clipboard

#----------------------------------------------------------------
# https://forum.opencv.org/t/filename-contains-character/3045/3
def imread_funny (filename):
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
def scaleImage (openName, screenWidth, screenHeight):
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

		tempImg = cv.copyMakeBorder(tempImg, topBottom, topBottom, leftRight, leftRight, cv.BORDER_CONSTANT, value=color)
		
		tempImg = cv.resize(tempImg, (screenWidth, screenHeight), cv.INTER_AREA)
	else:
		print (">>>> ERROR Unable to open ", openName)
	
	if (c != 3):
		success = False
		print (">>>> ERROR ", openName, " has color depth of ", c)
	
	if (args.gray != 0):
		tempImg = cv.cvtColor(tempImg, cv.COLOR_BGR2GRAY)
		tempImg = cv.cvtColor(tempImg, cv.COLOR_GRAY2BGR) # convert back because we still need a color depth of 3 
	
	return (tempImg, success)
#----------------------------------------------------------------

def blend (img1, img2, oddEven, fadeTime, duration):
		
		timeNextFrame = time.time() + videoInterval
		
		if oddEven:
			bright1 = 1
			bright2 = 0
		else:
			bright1 = 0
			bright2 = 1
		
		dst = cv.addWeighted(img1,bright1,img2,bright2,0)
		cv.imshow('dst',dst)

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

			dst = cv.addWeighted(img1,bright1,img2,bright2,0)
			cv.imshow('dst',dst)
			if ((args.output != '') and (time.time() > timeNextFrame)):
				out.write(dst)
				timeNextFrame = timeNextFrame + videoInterval

			tempKey = cv.waitKey(1) 
			if (tempKey != -1):
				key = tempKey
				
				if (tempKey == ord ('f')):
					freeze = not freeze
					if (freeze):
						timeBefore = time.time() - timeStart
						timeAfter = timeEnd - time.time()
				else:
					key = tempKey
					
					
		
		# blending finished
		
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
parser = argparse.ArgumentParser(description = "display all images in folder with nice transitions", epilog = "Esc/q=quit, p=pause on/off, c=copy filename to clipboard, f=freeze on/off, backspace=previous, space=next")
parser.add_argument("-p", "--path", type=str, default=".", help="path where images are found")
parser.add_argument("-s", "--subdirs", type=int, default=0, help="depth of subdirectories.  0 (default): no subdirs, -1: all subdirs")
parser.add_argument("-d", "--duration", type=float, default="5", help="time image is shown [seconds]. -1 for manual switching")
parser.add_argument("-f", "--fade", type=float, default="1.5", help="time of fading effect [seconds]")
parser.add_argument("-l", "--loop", type=int, default="1", help="nr. of loops, -1 = loop forever, default=1")
parser.add_argument("-m", "--mask", type=str, default=".", help="mask filename (regex syntax)")
parser.add_argument("-a", "--age",  type=float, default="-1.0", help="maximal age of file in days. -1.0 (default): all files")
parser.add_argument("-g", "--gray", type=int, default="0", help="0 (default): color, all else: convert to grayscale")
parser.add_argument("-r", "--random", type=int, default="0", help="random shuffle. 0 (default): sorted, all else: shuffeled")
parser.add_argument("-w", "--width", type=int, default="-1", help="width. -1 (default): automatic")
parser.add_argument("-hh", "--height", type=int, default="-1", help="height. -1 (default): automatic")
parser.add_argument("-o", "--output", type=str, default="", help="output video file (very experimental)")
parser.add_argument("--fps", type=float, default=30, help="fps of output video (very experimental)")
args = parser.parse_args()

extensionsPhoto = ('.png', '.jpg', '.jpeg', '.jfif', '.tiff', '.bmp' , '.webp', '.gif') 
steps = 50
key = 0

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

black = np.zeros((h+1, w+1, 3), np.uint8)
img1 = black
img2 = black
cv.imshow('dst',black)
cv.waitKey(1000)

oddEven = True

while ((loopCount < args.loop) or (args.loop == -1)):

	if (args.random != 0):
		print ("shuffle....")
		random.shuffle (filenames) 


	IndexFiles = 0
	running = True

	while ((IndexFiles >= 0) and (IndexFiles < NumFiles) and running):
		
		imgName = filenames[IndexFiles]
		
		print ('\nImage nr. ', IndexFiles, ' ', imgName)
		if oddEven:
			(img2, success) = scaleImage(imgName, w+1, h+1)
		else:
			(img1, success) = scaleImage(imgName, w+1, h+1)
		
		Back = False
		
		if (success):
			key = blend (img1, img2, oddEven, args.fade, args.duration)
			# print (key)
			if ((key == ord('q')) or (key == 27)):
				print ("interrupted by user")
				running = False

			elif ((key == ord('b')) or (key == 8)):
				Back = True
				key = -1
			elif (key == ord('c')):
				print ("copying ", imgName, " to clipboard")
				clipboard.copy (imgName)
				key = -1
				
			oddEven = not oddEven
		else:
			print ("Could not read file ", imgName)
			
			
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
blend (img1, img2, oddEven, 2 * args.fade, 0)

print ("Done.")
cv.destroyAllWindows()
if (args.output != ''):
	out.release()