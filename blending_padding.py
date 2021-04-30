# based on
# opencv tutorial --> coreOperations/OpenCV_%20Arithmetic%20Operations%20on%20Images.html

# todo:
# "image stabilisation" = zoom/pan/rotate similar images so they fit together 
# slowly pan pnoramic images across screen 
# option: manually input height and width 
# opencv cannot read a filename containing » 

# done: 
# subdirectries
# stop "3rd picture" while blending = freeze
# copy image path+name to clipboard
# loop: do not read and discard the directory every time 

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
	try: 
		f = open(filename, "rb")
		b = f.read()
		f.close()
		b = np.frombuffer(b, dtype=np.int8)
		image = cv.imdecode(b, cv.IMREAD_COLOR);
		return (image)
	except exception as e:
		print (e)
		return None



#----------------------------------------------------------------
# https://thispointer.com/python-how-to-get-list-of-files-in-directory-and-sub-directories/

'''
    For the given path, get the List of all files in the directory tree 
'''
def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles        

#----------------------------------------------------------------
def scaleImage (openName, screenWidth, screenHeight):
	# tempImg = cv.imread(openName)
	tempImg = imread_funny(openName)
	(h,w,c) = tempImg.shape
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
	
	return tempImg
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
parser.add_argument("-s", "--subdirs", type=int, default=0, help="subdirectories")
parser.add_argument("-d", "--duration", type=float, default="5", help="time image is shown [seconds]. 0 for manual switching")
parser.add_argument("-f", "--fade", type=float, default="1.5", help="time of fading effect [seconds]")
parser.add_argument("-l", "--loop", type=int, default="0", help="nr. of loops, -1 = loop forever, default=0")
parser.add_argument("-m", "--mask", type=str, default=".", help="mask filename")
parser.add_argument("-r", "--random", type=int, default="0", help="random shuffle")
args = parser.parse_args()

extensionsPhoto = ('.jpg', '.jpeg', 'jfif', '.tiff', '.bmp')
steps = 50

# Window in full-screen-mode, determie aspect ratio of screen
cv.namedWindow("dst", cv.WND_PROP_FULLSCREEN)
cv.setWindowProperty("dst",cv.WND_PROP_FULLSCREEN,cv.WINDOW_FULLSCREEN)
(a,b,w,h) = cv.getWindowImageRect('dst')
aspectRatioScreen =  (w+1) / (h+1)
print ('Screen: ', w+1, h+1, aspectRatioScreen)

loopCount = 0

if (args.subdirs > 0):
	fileList = getListOfFiles(args.path)
else:
	fileList = os.listdir(path=args.path)

filenames = []
for filename in fileList:
	if (filename.lower().endswith(extensionsPhoto)):
	# if ('.jpg' in filename.lower()):
		if (re.search(args.mask,filename)):
			if (args.subdirs > 0):
				filenames.append (filename)
			else:
				filenames.append (os.path.join(args.path, filename))

NumFiles = len(filenames)
print (NumFiles, "files found")
if (NumFiles == 0):
	exit()
filenames.sort()

key = 0

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
			img2 = scaleImage(imgName, w+1, h+1)
		else:
			img1 = scaleImage(imgName, w+1, h+1)
		
		Back = False
		
		key = blend (img1, img2, oddEven, args.fade, args.duration)
		print (key)
		if ((key == ord('q')) or (key == 27)):
			print ("End")
			break
		elif key == ord('p'):
			print ("Pause")
			cv.waitKey(0)
		elif ((key == ord('b')) or (key == 8)):
			Back = True
		elif (key == ord('c')):
			clipboard.copy (imgName)
		
		oddEven = not oddEven
			
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
		print ("End")
		break

		
cv.destroyAllWindows()