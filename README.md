# blend-images

Create a slide show of images in a folder with smooth transition between images

Download executable for Windows here, if you trust me: http://martinpi.at/games/utils/blending_padding.exe  (it is too large for GitHub),
compiled with [auto-py-to-exe](https://pypi.org/project/auto-py-to-exe/)

Written in Python3, using opencv

It started as an excercise in the [tutorial](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_core/py_image_arithmetics/py_image_arithmetics.html "Arithmetic Operations")

## Features:

* Optionally dig into subdirectories, 
* Optionally random-shuffle images, 
* Optionally loop through files, 
* Copy current path+filename to clipboard, 
* move back and forward, timed or on keypress, 
* stop transition to see "the third image"

## command line arguments

usage: blending_padding.py [-h] [-p PATH] [-s SUBDIRS] [-d DURATION] [-f FADE]
                           [-l LOOP] [-m MASK] [-r RANDOM]

display all images in folder with nice transitions

optional arguments:
*  -h, --help            show this help message and exit
*  -p PATH, --path PATH  path where images are found
*  -s SUBDIRS, --subdirs SUBDIRS
*                        subdirectories
*  -d DURATION, --duration DURATION
*                        time image is shown [seconds]. 0 for manual switching
*  -f FADE, --fade FADE  time of fading effect [seconds]
*  -l LOOP, --loop LOOP  nr. of loops, -1 = loop forever, default=0
*  -m MASK, --mask MASK  mask filename
*  -r RANDOM, --random RANDOM random shuffle
*  -w WIDTH, --width WIDTH
*                        width. -1 (default): automatic
*  -hh HEIGHT, --height HEIGHT
*                        height. -1 (default): automatic
*  (You need to specify both width and height, or leave both to default)                      
*
* Esc/q=quit, p=pause, c=copy filename to clipboard, f=freeze, backspace=previous, any other key=next

## Bugs and limitations
* Works well under Windows, problem with detecting screen size under Linux
* Todo's: see program code
