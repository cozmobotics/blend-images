# blendPics

## Overview

blendPics creates a slide show of images with smooth and/or interesting transition between images

Available as screensaver (NEW!) and standalone application

An example output is here: https://youtu.be/OLZAuHpUXRo

It is a console application which needs a little computer knowledge to use it. 

## Features:

* some transition types available. Try them out!
* Optionally dig into subdirectories, including .lnk-files (link under Windows),
* complex sorting methods available
* Optionally random-shuffle images, "mild shuffling" available
* Optionally loop through files, 
* Optionlly filter protrait or landscape images (for nicer transitions)
* Copy current path+filename to clipboard, 
* move back and forward, timed or on keypress,
* open current picture in default viewer by pressing Enter
* filter portrait or landscape images, filter newest files, add custom filter (regex)
* optionally read list of pictures from file 
* stop transition to see "the third image"
* No Ken Burns Effect (because I hate it)
* play videos (with external player)
* optionally write to video (experimental)
* compiled or interpreted (python) version available 
* no installation, just run the program (compiled version)
* leaves no trace on your PC
* optionally disable screensaver while show is running (Windows only)
* optionally leave screen black after last picture, wait for keypress

Tested under Windows 10. As Python and its libraries are cross-platform, the program should run under any other operating system as well. 

## how to get bledPics

As with most open source programs, you may download a compiled executable or get the source. 

### Download the executable
Download executable for Windows here, if you trust me: http://martinpi.at/games/utils/blendPics.exe and http://martinpi.at/games/utils/blendPicsScr.exe (it is too large for GitHub). I did my virus check with Avira. As with any download, please do your own virus-check. 

### use the source
In this repository you find the necessary files to use the python interpreter or compile from source. 

Written in Python3, using opencv 2. You will have to install some other libraries like exif. 

I compiled with [auto-py-to-exe](https://pypi.org/project/auto-py-to-exe/) / pyinstaller. There is Windows batch to compile and write the compile time into the executable. 

## Details

It started as an excercise in the [tutorial](https://docs.opencv.org/master/d0/d86/tutorial_py_image_arithmetics.html "Arithmetic Operations")

It is a console application which needs a little computer knowledge to use it. I suggest to put a batch file onto your desktop which calls blendPics like you prefer to use it, so you can drag a folder onto the batch to start the slideshow. Instructional video (in German) is here: https://youtu.be/I6BX8PdTSBU 

For installing the screensaver, see the comments in blendPicsScr.py 

__Although it is a console application, all keyboard input goes to the graphical window which must have the focus. The console window is for information only.__

## transitions
A detailed explanation of transitions is [here](transitions.md)

## sorting 
a detailed explanation of sorting is [here](sorting.md)

## command line arguments
* usage: blendPics.py [-h] [-p PATH] [-s SUBDIRS] [-d DURATION] [-f FADE]
                 [-t TRANSITION] [-m MATCH] [-M MATCH] [-n NOTMATCH]
                 [-N NOTMATCH] [-pl PORTRAIT_LANDSCAPE] [-l LOOP]
                 [--limit LIMIT] [-a AGE] [-g GRAY] [-r RANDOM] [-i INPUT]
                 [-v VERBOSE] [-o OUTPUT] [-w WIDTH] [-hh HEIGHT] [--fps FPS]
                 [-bg BACKGROUND] [-b BLACKOUT] [-ss SCREENSAVER] [-scr SCR]

* display all images in folder with nice transitions

* optional arguments:
*   -h, --help            show this help message and exit
*   -p PATH, --path PATH  path where images are found
*   -s SUBDIRS, --subdirs SUBDIRS
                        depth of subdirectories. 0 (default): no subdirs, -1:
                        all subdirs
 *  -d DURATION, --duration DURATION
                        time image is shown [seconds]. -1 for manual switching
*   -f FADE, --fade FADE  time of fading effect [seconds]
*   -t TRANSITION, --transition TRANSITION
                        types of transition. Combination of the letters
                        b,o,n,d,l,i,x
*   -m MATCH, --match MATCH
                        mask filename (regex syntax, case insensitive)
*   -M MATCH, --Match MATCH
                        mask filename (regex syntax, case sensitive)
*   -n NOTMATCH, --notmatch NOTMATCH
                        negative mask filename (regex syntax, case
                        insensitive)
*   -N NOTMATCH, --NotMatch NOTMATCH
                        negative mask filename (regex syntax, case sensitive)
*   -pl PORTRAIT_LANDSCAPE, --portrait_landscape PORTRAIT_LANDSCAPE
                        filter portrait or landscape. p = portrait, l =
                        landscape, pl (default) = both
*   -l LOOP, --loop LOOP  nr. of loops, -1 = loop forever, default=1
*   -a AGE, --age AGE     maximal age of file in days. -1.0 (default): all files
*   -g GRAY, --gray GRAY  0 (default): color, all else: convert to grayscale
*   -r RANDOM, --random RANDOM
                        random shuffle. -1 (default): leave as is, 0: sorted,
                        0..100: shuffle
*   -i INPUT, --input INPUT
                        input file, containing filenames and parameters
                        (script)
* -v VERBOSE, --verbose VERBOSE
                        verbose ... 0=only errors, 1=print filenames, 1=print
                        all data*   -v VERBOSE, --verbose VERBOSE
                        verbose ... 0=only errors, 1=print filenames, 1=print
                        all data, > 1 ... debug info
*   -o OUTPUT, --output OUTPUT
                        output video file (very experimental)
*   -w WIDTH, --width WIDTH
                        width. -1 (default): automatic
*   -hh HEIGHT, --height HEIGHT
                        height. -1 (default): automatic
*   --fps FPS             fps of output video (very experimental)
*   -bg BACKGROUND, --background BACKGROUND
                        background color in hex values (rgb) like #aabbcc
*  -bg BACKGROUND, --background BACKGROUND
                        background color in hex values (rgb) like #0fcc80
*  -b BLACKOUT, --blackout BLACKOUT
                        yes/no. At the end of the show, keep the window dark
                        until a key is pressed. Default = yes
*  -ss SCREENSAVER, --screensaver SCREENSAVER
                        yes/no. Disable screensaver. Default = yes
*   --scr SCR,          blendPics acts as screensaver (quit when a key is
                        pressed), Default=no
*  --log LOG             filename to log actions for debug purposes. Empty
                        string(default): do not log
*  --sort SORT          sorting options ... syntax: see https://github.com/cozmobotics/blend-images/blob/main/sorting.md
*  --videoplayer VIDEOPLAYER
                        external command to play video. Default: system
                        settings
*  --startimage STARTIMAGE
                        image name to start with (if not starting with first
                        image)

Esc/q=quit, p=pause on/off, f=freeze on/off, s(while blending)=save picture,
c=copy filename to clipboard, b/o/n/d/l=change transition, left arrow or
backspace=previous, right arrow or space=next, F2,F3,F4,F5=decrease/increase
fade-time/duration



## Bugs and limitations
* Works well under Windows, problem with detecting screen size under Linux
* No sound (music etc). 
* White line on top and left margin when running in full-screen
* No error detection when video is not writable (e.g. disk full)
* Todo's: see program code
* Screensaver's search directory is hard-coded to userdir/Pictures, configuration dialog is not yet implemented. 
  If the pictures you want to use for the screensaver are in a different directory, add a link (.lnk-file under Windows) in your Pictures directory
