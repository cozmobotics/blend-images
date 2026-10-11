''' 
   blendPicsScr 
   ************
   the blendPics screensaver 
   
   blendPics.py is an interactive Python script to display photos with interesting transitions.
   blendPicsScr is a Windows screensaver which uses plendPics. 
   Tested under Windows 10, so far.
   
   How to use:
   1) write your preferences into the structure "arguments" below (refer to blendPics help screen)
   2) create an exe file (you can use auto-py-to-exe) 
   3) rename blendPicsScr.exe to blendPicsScr.scr 
   4) in a Windows file manager (like Windows Explorer) right-click on blendPicsScr.scr and select "install" 
'''

import blendPics 
from collections import namedtuple
import sys
import os

# for count in range (len(sys.argv)):
	# print ("argument " + str(count) + ": " + sys.argv[count])


if len(sys.argv) > 1:
	# print (sys.argv[1])
	if sys.argv[1].startswith ("/s"):
		print ("screensaver in full-screen mode")
	if sys.argv[1].startswith ("/p"):
		print ("screensaver preview")
	if sys.argv[1].startswith ("/c"):
		print ("screensaver configuration dialog")
		print ("not yet implemented")
		input ("Press Enter to continue")
		sys.exit()
	
homeDir = os.path.expanduser("~")
pictDir = os.path.join (homeDir, "Pictures")
# logFile = ""
logFile = os.path.join (homeDir, "blendPicsScr_log.txt")

arguments = namedtuple ( 
	"arguments", 
	"path delimiter subdirs duration fade transition all match Match notmatch NotMatch portrait_landscape  enlargeloop limit age gray random input verbose output width height fps background blackout screensaver scr log sort videoplayer startimage audio"
	)
	
# arguments.path = "d:/Digi_phot/"
arguments.path = pictDir
arguments.delimiter = "#"
arguments.subdirs = -1
arguments.duration = 15
arguments.fade = 3
arguments.transition = "all"
arguments.match = "."
arguments.Match = "."
arguments.notmatch = ""
arguments.NotMatch = ""
arguments.portrait_landscape  = "pl"
arguments.enlarge = "no"
arguments.loop = -1
arguments.limit = -1
arguments.age = -1.0
arguments.gray = 0
arguments.random = 100
arguments.input = ""
arguments.verbose = 1
arguments.output = ""
arguments.width = -1
arguments.height = -1
arguments.MinSize = 50  # 2026-09-15
arguments.fps = 30.0
arguments.background = "#000000"
arguments.blackout = "no"
arguments.screensaver = "no"
arguments.scr = "yes"
# arguments.log = logFile
arguments.log = ""
arguments.sort = ""
arguments.videoplayer = "none"
arguments.startimage = ""
arguments.audio = ""


	
blendPics.doIt (arguments)