

import argparse
import sys
import os
import re
from datetime import datetime # for logfile
import getPics

#-----------------------------------------------------------------------------------------------------
def doIt (argumentsDoIt):
	extensionsPhoto = ('.png', '.jpg', '.jpeg', '.jfif', '.tiff', '.bmp' , '.webp', '.gif') 
	extensionsVideo = ('.mp4', '.mpeg', '.avi', '.mov','.mts') 

	now = datetime.now()
	print ('# current working directory: ', os.getcwd(), ', command line parameters:', args)

	filenamesAll = []

	if (args.input == ''):
		paths = args.path.split ('#')
		for path in paths:
			print ("# searching images on " + path)
			fileList = getPics.getListOfFiles(path, args.subdirs)

			for filename in fileList:
				addFile = True
				if ((filename.lower().endswith(extensionsPhoto)) or (filename.lower().endswith(extensionsVideo))):  #+++ use os.path.splitext
					if (not re.search(args.match,filename,flags=re.IGNORECASE)):
						addFile = False
					if (not re.search(args.Match,filename)):
						addFile = False
					if (args.notmatch != '' and re.search(args.notmatch,filename,flags=re.IGNORECASE)):
						addFile = False
					if (args.NotMatch != '' and re.search(args.NotMatch,filename)):
						addFile = False
					if (args.age > 0):
						age = time.time() - os.path.getmtime(filename) ### +++ aus exif nehmen
						age = age / 3600 / 24 # age in days
						# print ("age: ",age," max age:" , args.age, addFile, age > args.age)
						if (age > args.age):
							addFile = False
					if (addFile):
						filenamesAll.append (filename)
					
	else:
		if args.input.lower().endswith('.xlsx'):
			filenamesAll = fromSpreadsheet (args.input)
		else: 
			try:
				inputList = open (args.input,'r')
			except Exception as e:
				print (e)
				sys.exit() 
			
			filenames = inputList.readlines()
			
			# filenames = ""
			# while True:
				# try:
					# next_line = inputList.readline()
				# except Exception as e:
					# print (str(e))
				# else:
					# print(next_line.strip()) # debug
					# filenames = filenames + next_line
				# if not next_line:
					# break;
					

			inputList.close()
			
			for filename in filenames:
				# 2023-02-13
				if '#' in filename:
					(a,b) = filename.split('#', 1)
					filename = a
				filename = filename.strip()  # to avoid blank lines on the screen 
				filenamesAll.append (filename)
			# filenamesAll = filenames
			inputList.close()

	fadeTime = args.fade
	NumFiles = len(filenamesAll)
	durationTime = args.duration
	LenShow = int (NumFiles * (fadeTime + durationTime) / 60)

	if ((args.limit > 0) and (args.limit < LenShow)):
		probability = 100 * args.limit / LenShow  # +++ inaccurate! Take fade time into account!
	else:
		probability = 100
	# print ("probability ", probability)

	# if (args.verbose >= 1):
		# print (NumFiles, "files found", " total duration approx", LenShow, " minutes,  limiting to ", args.limit, " minutes. Probability=", int(probability), "%")
	print ("# " + str(NumFiles) + " files found," + " total duration approx " + str(LenShow) + " minutes, limiting to " + str(args.limit) + " minutes, Probability=" + str(int(probability)) + "%")
	if (NumFiles == 0):
		print ("No images fund!")
		sys.exit()

	filenames = getPics.bubbleShuffle (filenamesAll, args.random, probability, args.sort)

	
	for filename in filenames:
		print (filename)
#-----------------------------------------------------------------------------------------------------
if __name__ == "__main__":

	if (len(sys.argv) == 2) and not (sys.argv[1].startswith('-')):		# only one command line argument given
		args = namedtuple ( 
		"arguments", 
		"path subdirs duration fade transition all match Match notmatch NotMatch portrait_landscape  enlargeloop limit age gray random input verbose output width height fps background blackout screensaver scr log sort videoplayer startimage"
		)
		
		args.path = "."
		args.subdirs = -1

		args.duration = 5
		args.fade = 1.5
		args.transition = "all"
		args.match = "."
		args.Match = "."
		args.notmatch = ""
		args.NotMatch = ""
		args.portrait_landscape  = "pl"
		args.enlarge = "no"
		args.loop = 1
		args.limit = -1
		args.age = -1.0
		args.gray = 0
		args.random = 0
		args.input = ""
		args.verbose = 1
		args.output = ""
		args.width = -1
		args.height = -1
		args.fps = 30.0
		args.background = "#000000"
		args.blackout = "yes"
		args.screensaver = "yes"
		args.scr = "no"
		args.log = ""
		args.sort = ""
		args.videoplayer = ""
		args.startimage = ""
		args.audio = ""

		singleArgument = sys.argv[1]
		
		if os.path.isfile(singleArgument):
			args.input = singleArgument
		elif os.path.isdir(singleArgument):
			args.path = singleArgument # this one and only parameter is the path
		else:
			print (singleArgument, "is neither a file nor a diretory")
			print ("Hit enter to quit ")
			input()
			sys.exit()
		


	else: # more than one argument
		parser = argparse.ArgumentParser(description = "test getPics",  )
		parser.add_argument("-p", "--path", type=str, default=".", help="path where images are found. Multiple pths can be separated by #")
		parser.add_argument("-s", "--subdirs", type=int, default=0, help="depth of subdirectories.  0 (default): no subdirs, -1: all subdirs")
		parser.add_argument("-d", "--duration", type=float, default="5", help="time image is shown [seconds]. -1 for manual switching")
		parser.add_argument("-f", "--fade", type=float, default="1.5", help="time of fading effect [seconds]")
		parser.add_argument("-m", "--match", type=str, default=".", help="mask filename (regex syntax, case insensitive)")
		parser.add_argument("-M", "--Match", type=str, default=".", help="mask filename (regex syntax, case sensitive)")
		parser.add_argument("-n", "--notmatch", type=str, default="", help="negative mask filename (regex syntax, case insensitive)")
		parser.add_argument("-N", "--NotMatch", type=str, default="", help="negative mask filename (regex syntax, case sensitive)")
		parser.add_argument("-pl", "--portrait_landscape", type=str, default="pl", help="filter portrait or landscape. p = portrait, l = landscape, pl (default) = both")
		parser.add_argument("-L", "--limit", type=int, default="-1", help="limit length of show to minutes (approx.) by randomly skipping images and maintaining the order ")
		parser.add_argument("-a", "--age",  type=float, default="-1.0", help="maximal age of file in days. -1.0 (default): all files")
		parser.add_argument("-r", "--random", type=int, default="-1", help="random shuffle. -1 (default): leave as is = depth-first-search, 0: sorted, 0..100: shuffle")
		parser.add_argument("-i", "--input", type=str, default="", help="input file, containing filenames [and parameters] (script)")
		parser.add_argument("-v", "--verbose", type=int, default="1", help="verbose ... 0=only errors, 1(Default)=print filenames, higher numbers = more information")
		parser.add_argument("--log", type=str, default="", help="filename to log actions for debug purposes. Empty string(default): do not log")
		parser.add_argument ("--sort", type=str, default="", help="sorting options ... syntax: see https://github.com/cozmobotics/blend-images/blob/main/sorting.md")
		parser.add_argument ("--startimage", type=str, default="", help="image name to start with (if not starting with first image)")
		

		args = parser.parse_args(sys.argv[1:]) # sys.argv[1:] for enabling help in compiled version

	black = None
	startImageFound = False
	doIt (args)

