# blend-images

Create a slide show of images in a folder with smooth transition between images

Download executable for Windows here, if you trust me: http://martinpi.at/games/utils/blending_padding.exe  (it is too large for GitHub),
compiled with [auto-py-to-exe](https://pypi.org/project/auto-py-to-exe/)

Written in Python3, using opencv

It started as an excercise in the [tutorial](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_core/py_image_arithmetics/py_image_arithmetics.html "Arithmetic Operations")

It is a console application which needs a little computer knowledge to use it. I suggest to put a batch file onto your desktop which calls blending_padding like you prefer to use it, so you can drag a folder onto the batch to start the slideshow. I plan to add an instructional video. 

## Features:

* Optionally dig into subdirectories, 
* Optionally random-shuffle images, 
* Optionally loop through files, 
* Copy current path+filename to clipboard, 
* move back and forward, timed or on keypress, 
* stop transition to see "the third image"

## command line arguments

usage: blending_padding.exe [-h] [-p PATH] [-s SUBDIRS] [-d DURATION]
                            [-f FADE] [-l LOOP] [-m MASK] [-a AGE] [-g GRAY]
                            [-r RANDOM] [-w WIDTH] [-hh HEIGHT] [-o OUTPUT]
                            [--fps FPS]

display all images in folder with nice transitions

optional arguments:
*  -h, --help            show this help message and exit
*  -p PATH, --path PATH  path where images are found
*  -s SUBDIRS, --subdirs SUBDIRS
                        depth subdirectories. 0 (default): no subdirs, -1: all
                        subdirs
*  -d DURATION, --duration DURATION
                        time image is shown [seconds]. 0 for manual switching
*  -f FADE, --fade FADE  time of fading effect [seconds]
*  -l LOOP, --loop LOOP  nr. of loops, -1 = loop forever, default=0
*  -m MASK, --mask MASK  mask filename (regex syntax)
*  -a AGE, --age AGE     maximal age of file in days. -1.0 (default): all files
*  -g GRAY, --gray GRAY  0 (default): color, all else: convert to grayscale
*  -r RANDOM, --random RANDOM
                        random shuffle. 0 (default): sorted, all else:
                        shuffeled
*  -w WIDTH, --width WIDTH
                        width. -1 (default): automatic
*  -hh HEIGHT, --height HEIGHT
                        height. -1 (default): automatic
*  -o OUTPUT, --output OUTPUT
                        output video file (very experimental)
*  --fps FPS             fps of output video (very experimental)

* Esc/q=quit, p=pause, c=copy filename to clipboard, f=freeze,
backspace=previous, space=next
## Bugs and limitations
* Works well under Windows, problem with detecting screen size under Linux
* Todo's: see program code
