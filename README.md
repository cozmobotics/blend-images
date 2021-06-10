# blend-images

Create a slide show of images with smooth transition between images

An example output is here: https://youtu.be/OLZAuHpUXRo

Download executable for Windows here, if you trust me: http://martinpi.at/games/utils/blendPics.exe  (it is too large for GitHub),
compiled with [auto-py-to-exe](https://pypi.org/project/auto-py-to-exe/) / pyinstaller

Written in Python3, using opencv

It started as an excercise in the [tutorial](https://docs.opencv.org/master/d0/d86/tutorial_py_image_arithmetics.html "Arithmetic Operations")

It is a console application which needs a little computer knowledge to use it. I suggest to put a batch file onto your desktop which calls blending_padding like you prefer to use it, so you can drag a folder onto the batch to start the slideshow. Instructional video (in German) is here: https://youtu.be/I6BX8PdTSBU 

__Although it is a console application, all keyboard input goes to the graphical window which must have the focus. The console window is for information only.__

## Features:

* some transition types available. Try them out!
* Optionally dig into subdirectories, 
* Optionally random-shuffle images, "mild shuffling" available
* Optionally loop through files, 
* Optionlly filter protrait or landscape images (for nicer transitions)
* Copy current path+filename to clipboard, 
* move back and forward, timed or on keypress, 
* filter portrait or landscape images, filter newest files, add custom filter (regex)
* optionally read list of pictures from file 
* stop transition to see "the third image"
* No Ken Burns Effect (because I hate it)
* optionally write to video (experimental)
* comiled or interpreted (python) version available 
* no installation, just run the program (compiled version)
* leaves no trace on your PC

A detailed explanation of transitions is [here](transitions.md)

## command line arguments
* usage: blendPics.py [-h] [-p PATH] [-s SUBDIRS] [-d DURATION] [-f FADE]
                    [-t TRANSITION] [-m MATCH] [-M MATCH] [-n NOTMATCH]
                    [-N NOTMATCH] [-pl PORTRAIT_LANDSCAPE] [-l LOOP] [-a AGE]
                    [-g GRAY] [-r RANDOM] [-i INPUT] [-v VERBOSE] [-o OUTPUT]
                    [-w WIDTH] [-hh HEIGHT] [--fps FPS] [-bg BACKGROUND]

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
