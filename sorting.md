# Using the parameter --sort

The parameter --sort takes a group of sorting options. 
If no sorting and no shuffling is specified, blendPics takes the files as they are given by the operating system. 
This may be convenient for you, otherwise use the sort feature. 

The **basic syntax** is: --sort keyword:option1[:option2][;keyword:option1[:option2][...]

Multiple sorting keywords (separated by semicolons) result in consecutive sort operations. 

## Keywords and options: 
* **name**
   ... just the filename including path, case sensitive. No more options, except for the option "down".  
* **os** ... Information from the operating system. Option1 may be:
  * time ... file date and time
  * dir ... directory (part of filename before the last / or \\)
  * file ... filename, ignoring the directory 
* **exif** ... Meta information given by the camera. Option1 may be: 
  * time
  * any other string which is reported by your camera, like f_number or focal_length_in_35mm_film (whatever sense it will make)
* **pic** ... the picture itself. Option1 may be:
  * hue ... average color. You may want to have all sunset pictures together.
  * sat ... average saturation. You may want to have the black-and-white images together
  * val ... average brightness. You may want to avoid big changes in brightness by using this option.
  * asp ... aspect ratio. You may want to avoid jumping too much between portrait and landscape
  * size ... total size, calculated as width*height 


## reverse sorting
To all sorting options you may add :down which reverses the sort order.

## Examples: 

> --sort os:time

will show the oldest pictures first and the newest pictures last 

> --sort pic:asp:down

will show the lanscape images first and then portrait images

## Multiple sorting

The sorting options are executed in the same order they are given in the parameter, separated by colons (:). Later sortings may (partially) override the previous ones. The last sort will "win".

According to the Python's [documentation](https://docs.python.org/3/howto/sorting.html#sort-stability-and-complex-sorts), *sorts are guaranteed to be stable. That means that when multiple records have the same key, their original order is preserved*. 

For example, if you want to see images of the first directory, then the ones from the second directory and so on, and within directories you want to see the newest image first and the oldest last, your sort parameter will look like this: 

> --sort os:time:down;os:dir

# random (shuffle)
If you use sorting **and** random, the shuffling will be applied after sorting. You may sort and then apply a mild shuffling like --random 10, which will more or less keep the sorted order, but make it less strict. This could be an interesting effect.  
