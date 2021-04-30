# blend-images

Create a slide show of images in a folder with smooth transition between images

Written in Python3, using opencv

* Optionally dig into subdirectories, 
* Optionally random-shuffle images, 
* Optionally loop through files, 
* Copy current path+filename to clipboard, 
* move back and forward, timed or on keypress, 
* stop transition to see "the third image"

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
*
* Esc/q=quit, p=pause, c=copy filename to clipboard, f=freeze,
*backspace=previous, any other key=next
