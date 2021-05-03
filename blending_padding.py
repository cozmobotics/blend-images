# based on
# opencv tutorial --> coreOperations/OpenCV_%20Arithmetic%20Operations%20on%20Images.html

# todo:
# "image stabilisation" = zoom/pan/rotate similar images so they fit together 
# slowly pan pnoramic images across screen 
# limit depth of subdirs
# img1/img2/oddEven --> imgNew/imgOld
# do not enlarge small pictures 
# display information (height/width, date, filename,...) 
# graphical menu 

# done: 
# subdirectries
# stop "3rd picture" while blending = freeze
# copy image path+name to clipboard
# loop: do not read and discard the directory every time 
# opencv cannot read a filename containing funny characters like » 
# option: manually input height and width 
# error handling ... AttributeError: 'NoneType' object has no attribute 'shape'
# Error when blendig images with different color depths (ignore images with color depth other than 3)

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
	
	return (tempImg, success)
#----------------------------------------------------------------

def blend (img1, img2, oddEven, fade, duration):
		global bright1
		global bright2
		
		timeSlice = 20 # milliseconds
		steps = int (fade * 1000 / timeSlice) + 1 # +1 to avoid division by zero
		increment = 1.0 / steps
		key = -1
		
		for n in range (steps):
			# print (img1.shape,img2.shape)
			dst = cv.addWeighted(img1,bright1,img2,bright2,0)
			cv.imshow('dst',dst)
			tempKey = cv.waitKey(int(1000 * fade/steps) + 1) # +1 to avoid waitKey(0) which would wait forever
			if (tempKey != -1):
				key = tempKey
				
				if (tempKey == ord ('f')):
					cv.waitKey(0)
					tempKey = ''

			if oddEven:
				bright1 = bright1 - increment
				bright2 = bright2 + increment
			else:
				bright1 = bright1 + increment
				bright2 = bright2 - increment
		
		if (key == -1):
			key = cv.waitKey(int(1000 * duration))
		return (key)


#----------------------------------------------------------------
parser = argparse.ArgumentParser(description = "display all images in folder with nice transitions", epilog = "Esc/q=quit, p=pause, c=copy filename to clipboard, f=freeze, backspace=previous, any other key=next")
parser.add_argument("-p", "--path", type=str, default=".", help="path where images are found")
parser.add_argument("-s", "--subdirs", type=int, default=0, help="subdirectories  0 (default): no subdirs, all else: recursively read all subdirs")
parser.add_argument("-d", "--duration", type=float, default="5", help="time image is shown [seconds]. 0 for manual switching")
parser.add_argument("-f", "--fade", type=float, default="1.5", help="time of fading effect [seconds]")
parser.add_argument("-l", "--loop", type=int, default="0", help="nr. of loops, -1 = loop forever, default=0")
parser.add_argument("-m", "--mask", type=str, default=".", help="mask filename (regex syntax)")
parser.add_argument("-r", "--random", type=int, default="0", help="random shuffle. 0 (default): sorted, all else: shuffeled")
parser.add_argument("-w", "--width", type=int, default="-1", help="width. -1 (default); automatic")
parser.add_argument("-hh", "--height", type=int, default="-1", help="height. -1 (default); automatic")
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


loopCount = 0

print ("searching images...")
# if (args.subdirs != 0):
	# fileList = getListOfFiles(args.path)
# else:
	# fileList = os.listdir(path=args.path)
	
fileList = getListOfFiles(args.path, args.subdirs)

filenames = []
for filename in fileList:
	if (filename.lower().endswith(extensionsPhoto)):
		if (re.search(args.mask,filename)):
			filenames.append (filename)
		
		# trying some more sophistivated evaluation, especially when doing a negative lookahead assertion
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

while ((loopCount <= args.loop) or (args.loop == -1)):

	if (args.random != 0):
		print ("shuffle....")
		random.shuffle (filenames) 

	black = np.zeros((h+1, w+1, 3), np.uint8)
	img1 = black
	img2 = black

	cv.imshow('dst',black)
	cv.waitKey(1000)

	oddEven = True
	increment = 1 / steps
	bright1 = 1.0
	bright2 = 0.0

	IndexFiles = 0
	oldName = ""

	while ((IndexFiles >= 0) and (IndexFiles < NumFiles)):
		
		imgName = filenames[IndexFiles]
		
		print ('\nBild nr. ', IndexFiles, ' ', imgName)
		if oddEven:
			(img2, success) = scaleImage(imgName, w+1, h+1)
		else:
			(img1, success) = scaleImage(imgName, w+1, h+1)
		
		Back = False
		
		if (success):
			key = blend (img1, img2, oddEven, args.fade, args.duration)
			print (key)
			if ((key == ord('q')) or (key == 27)):
				print ("break loop")
				break
			elif key == ord('p'):
				print ("Pause")
				cv.waitKey(0)
				key = 0
			elif ((key == ord('b')) or (key == 8)):
				Back = True
				key = 0
			elif (key == ord('c')):
				print ("copying ", imgName, " to clipboard")
				clipboard.copy (imgName)
				key = 0
				
			oddEven = not oddEven
		else:
			print ("Could not read file ", imgName)
			
			
		if (Back):
			IndexFiles = IndexFiles - 1
		else:
			IndexFiles = IndexFiles + 1

	if (oddEven):
		img2 = black
	else:
		img1 = black
	blend (img1, img2, oddEven, args.fade, 1.0)

	loopCount = loopCount + 1

	if ((key == ord('q')) or (key == 27)):
		print ("break")
		break

print ("Done.")
cv.destroyAllWindows()