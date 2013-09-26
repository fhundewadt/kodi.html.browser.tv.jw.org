
"""
import xbmcgui

 
count = len(sys.argv) - 1
 
if count > 0:
	xbmcgui.Dialog().ok("Status",sys.argv[0] +" called with " + str(count)+" args",
		"["+", ".join(sys.argv[1:])+"]")
else:
	xbmcgui.Dialog().ok("Status","no arguments specified")
"""
# Thanks to http://xbmc-scripting.googlecode.com/svn/trunk/IRCXBMC/default.py
import xbmcgui
import sys

try: Emulating = xbmcgui.Emulating
except: Emulating = False 
 
class Example(xbmcgui.WindowDialog): 

    def __init__(self,):
        if Emulating: xbmcgui.Window.__init__(self)
        self.abouttitle = xbmcgui.ControlLabel(340, 135, 300, 30, str(sys.argv) )
        self.addControl(self.abouttitle)
        
    def onControl(self, c):
        if self.h1 == c:
            print "hey"
        if self.something == c:
            print "you press med"
        if self.btn_quit == c:
            self.close()
 
Z = Example()
Z.doModal()
del Z
