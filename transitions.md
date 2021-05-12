# Transitions

blendPics offers some transitions between images. 
There are two kinds: __Blending__ and __masking__. 

And, no, we don't do roll from left to right and right to left, scroll and jalousie, and so on. We have far more interesting transitions. 

## Blending

This mimics the goog old slide shows with two slide projectors. The old picture gets darker while the new picture gets lithter until only the new picture is visible. 
This was done to eliminate the dark pause and on some projectors the shifting out and in. 

## Masking

A more sophisticated way to change from one picture to the other is crating a mask which defines which part of the screen shows the old picture and which part shows the new picture. 
So far, this is not unlike the (boring) scroll, roll and so non effects. 

blendPics generates the mask from one of the pictures and fills in the new picture. 

There are a few possibilities to choose from. 

### Old or new

The mask can be generated from the old or from the new picture. 

* If you specivy __old__, the new picture begins to fill up the dark or light sections of the old picture (dark or light, see next paragraph). 
__old__ is the more gentle way of transition.
* If you specify __new__, the new picture starts indepedently of the old picture. This is the mor aggressive way. 

### Light or dark

This option lets you decide if the light or the dark parts of the picture are the first ones to get replaced ("old") or be the first to appear ("new"). 

If you shoose old and dark, you get a strange effect on portraits: The eyes are usually dark, and they are among the first parts where the new picture shines through. 
This looks spooky. You may like it or not. 

### The syntax of the --transition parameter

The parameter --transition or -t accepts a string which may consitst of the letters b,o,n,d,l. 

The order of the letters is not relevant, "ol" is the same as "lo". If there are excessive characters like "x" or so, they are ignored. 
Doubling a letter makes no sense, the second occurance of a letter will revert the effect of the first one. 

By default, all effects are enabled. You can change this by supplying a --transition or -t parameter. If more than one possibility exists, the effect is chosen randomly. 

__b__ turns the normal blending on 

__o__ means "old image" as explained above 

__n__ means "new image" as explained above. At least one of the options o and n must be enabled. 

__d__ meand darker parts of the image  as explained above. 

__l__ means lighter parts of the image  as explained above . At least one of the options d and l must be enabled. 

So, you can specify combinations like "-t onl" or "-t nd". 

If you write "-t on" without giving an instruction for light or dark, this is invalid. Same to "-t dl" owthout o or n. 
In this case, blendPics falls back to blending. So, if you expect masking and only get blending, this will be the cause. 

### Changing the transitions at runtime

You can change the effects while the show is playing. Press any of the keys b,o,n,d,l to change an option. 
This takes effect on the next transition. 

If an option is already enabled, it will be disabled. If you disable both o and n or both l and d, blendPics falls back to blending. 
