

import ctypes  # fuer MessageBox   

import platform
#import os
#import sys

def messagebox (prompt, caption="", type=1):
	osName = platform.platform(terse=True)
	if "Windows" in osName: 
		retVal = ctypes.windll.user32.MessageBoxW(0, prompt, caption, type)   # https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-messageboxw
	else:
		retVal = -1
	return retVal