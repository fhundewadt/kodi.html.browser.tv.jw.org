"""
WEEK PROGRAM RELATED FUNCTIONS
"""
import xbmc
import xbmcgui
import xbmcplugin

import os
import jw_config
import jw_common
import re

# Show daily text 
def showWeekProgram(date):

    language    = jw_config.language
    json_url    = jw_config.const[language]["daily_text_json"] + "/" + date

    json  = jw_common.loadJsonFromUrl(json_url)
    text  = jw_common.t(30035) + "\n"
    text  = text + json["items"][1]["content"] # there is a trailing \n in the item text
    text  = text + jw_common.t(30028)
    text  = text + "\n" +  json["items"][2]["content"]
    text  = jw_common.cleanUpText(text).encode("utf8") 

    dialog = WeekProgram()
    dialog.customInit(text);
    dialog.doModal();
    del dialog

    xbmc.executebuiltin('Action("back")')


# Window showing daily text
class WeekProgram(xbmcgui.WindowDialog):

    def __init__(self):
        if jw_config.emulating: xbmcgui.Window.__init__(self)

    def customInit(self, text):
        
        border = 50; # px relative to 1280/720 fixed grid resolution

        # width is always 1280, height is always 720.
        # getWidth() and getHeight() instead read the REAL screen resolution
        bg_image = jw_config.dir_media + "blank.png"
        self.ctrlBackgound = xbmcgui.ControlImage(
            0,0, 
            1280, 720, 
            bg_image
        )
        self.ctrlText= xbmcgui.ControlTextBox(
            border, border, 
            1280 - border *2, 720 - border, 
            'font30', "0xFF000000"
        )
        
        self.addControl (self.ctrlBackgound)
        self.addControl (self.ctrlText)

        self.ctrlText.setText( self.getProgram(text) );

    #get actioncodes from https://github.com/xbmc/xbmc/blob/master/xbmc/guilib/Key.h
    def onAction(self, action):
        #Every key will close the windo
        self.close()
        return

    # Grep today's textual date
    def getProgram(self, text):

        clean = re.sub("<([^>]*)>", "", text)
        spaced = re.sub("\n", "\n\n", clean)
        return spaced
