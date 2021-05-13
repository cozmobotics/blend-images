# blend-images

Create a slide show of images in a folder with smooth transition between images

An example output is here: https://youtu.be/OLZAuHpUXRo

Download executable for Windows here, if you trust me: http://martinpi.at/games/utils/blendPics.exe  (it is too large for GitHub),
compiled with [auto-py-to-exe](https://pypi.org/project/auto-py-to-exe/) / pyinstaller

Written in Python3, using opencv

It started as an excercise in the [tutorial](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_core/py_image_arithmetics/py_image_arithmetics.html "Arithmetic Operations")

It is a console application which needs a little computer knowledge to use it. I suggest to put a batch file onto your desktop which calls blending_padding like you prefer to use it, so you can drag a folder onto the batch to start the slideshow. I plan to add an instructional video. 

## Features:

* some transition types available. Try them out!
* Optionally dig into subdirectories, 
* Optionally random-shuffle images, 
* Optionally loop through files, 
* Optionlly filter protrait or landscape images (for nicer transitions)
* Copy current path+filename to clipboard, 
* move back and forward, timed or on keypress, 
* filter portrait or landscape images, filter newest files, add custom filter (regex)
* stop transition to see "the third image"
* No Ken Burns Effect (because I hate it)
* optionally write to video (experimental)
* comiled or interpreted (python) version available 
* no installation, just run the program (compiled version)
* leaves no trace on your PC

A detailed explanation of transitions is [here](transitions.md)

## command line arguments

* usage: blendPics.exe [-h] [-p PATH] [-s SUBDIRS] [-d DURATION] [-f FADE]
                     [-t TRANSITION] [-m MASK] [-pl PORTRAIT_LANDSCAPE]
                     [-l LOOP] [-a AGE] [-g GRAY] [-r RANDOM] [-w WIDTH]
                     [-hh HEIGHT] [-o OUTPUT] [--fps FPS]

* display all images in folder with nice transitions

* optional arguments:
*   -h, --help            show this help message and exit
*   -p PATH, --path PATH  path where images are found
*   -s SUBDIRS, --subdirs SUBDIRS
                        depth of subdirectories. 0 (default): no subdirs, -1:
                        all subdirs
*   -d DURATION, --duration DURATION
                        time image is shown [seconds]. -1 for manual switching
*   -f FADE, --fade FADE  time of fading effect [seconds]
*   -t TRANSITION, --transition TRANSITION
                        types of transition. Combination of the letters
                        b,o,n,d,l
*   -m MASK, --mask MASK  mask filename (regex syntax)
*   -pl PORTRAIT_LANDSCAPE, --portrait_landscape PORTRAIT_LANDSCAPE
                        filter portrait or landscape. p = portrait, l =
                        landscape, pl (default) = both
*   -l LOOP, --loop LOOP  nr. of loops, -1 = loop forever, default=1
*   -a AGE, --age AGE     maximal age of file in days. -1.0 (default): all files
*   -g GRAY, --gray GRAY  0 (default): color, all else: convert to grayscale
*   -r RANDOM, --random RANDOM
                        random shuffle. 0 (default): sorted, all else:
                        shuffeled
*   -w WIDTH, --width WIDTH
                        width. -1 (default): automatic
*   -hh HEIGHT, --height HEIGHT
                        height. -1 (default): automatic
*   -o OUTPUT, --output OUTPUT
                        output video file (very experimental)
*   --fps FPS             fps of output video (very experimental)

*   -bg BACKGROUND, --background BACKGROUND
                        background color in hex values (rgb) like #aabbcc

* Esc/q=quit, p=pause on/off, f=freeze on/off, c=copy filename to clipboard,
b/o/n/d/l=change transition, backspace=previous, space=next


## Bugs and limitations
* Works well under Windows, problem with detecting screen size under Linux
* Transition type mask: On some images, parts of the old image remain
* Todo's: see program code
