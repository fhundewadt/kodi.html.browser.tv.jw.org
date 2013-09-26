"""
EXECUTABLE RELATED FUNCTION
"""
import xbmc
import xbmcgui
import xbmcplugin

import os
import jw_config
import jw_load
import re
import urllib
import datetime

now = datetime.datetime.now()

# List of available executable  services
def showExecIndex(language):

    # 1. Dailiy Text
    now 			= datetime.datetime.now()
    date_for_json 	= str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    date_format 	= jw_config.const[language]["date_format"]
    title 			= jw_config.t(30012)  + " - " + now.strftime(date_format)
    listItem 		= xbmcgui.ListItem( title )
    params  		= {
        "content_type"  : "executable", 
        "mode" 			: "open_daily_text",
        "date"			: date_for_json
    } 
    url = jw_config.plugin_name + '?' + urllib.urlencode(params)
    xbmcplugin.addDirectoryItem(
        handle		= jw_config.pluginPid, 
        url			= url, 
        listitem	= listItem, 
        isFolder	= True 
    )  

    xbmcplugin.endOfDirectory(handle=jw_config.pluginPid)


# Show daily text 
def showDailyText(language, date):

    json_url = jw_config.const[language]["daily_text_json"] + "/" + date
    json = jw_load.loadJsonFromUrl(json_url)
    text = json["items"][0]["content"]

    dialog = DailiyText()
    dialog.customInit(text);
    dialog.doModal();
    del dialog
    xbmc.executebuiltin('Action("back")')

# Window showing daily text
class DailiyText(xbmcgui.WindowDialog):

    def __init__(self):
        if jw_config.emulating: xbmcgui.Window.__init__(self)

    def customInit(self, text):
        
        width = self.getWidth()
        height = self.getHeight()

        self.ctrlData= xbmcgui.ControlTextBox(
            50 ,0, 
            width - 100, 30, 
            'font24_title', "0xFF0000FF"
        )
        self.ctrlScripture= xbmcgui.ControlTextBox(
            50 ,40, 
            width - 100, 100, 
            'font24_title', "0xFF000000"
        )
        self.ctrlText= xbmcgui.ControlTextBox(
            50,150, 
            width - 100, height - 150, 
            'font13', "0xFF000000"
        )
        bg_image = jw_config.dir_media + "blank.png"
        self.ctrlBackgound = xbmcgui.ControlImage(0,0, width, height, bg_image)
        
        self.addControl(self.ctrlBackgound)
        self.addControl (self.ctrlData)
        self.addControl (self.ctrlScripture)
        self.addControl (self.ctrlText)

        self.ctrlData.setText( self.getFirstLine(text) );
        self.ctrlScripture.setText( self.getScriptureLine(text) );
        self.ctrlText.setText( self.getComment(text) );

    def onAction(self, action):
        self.close()

    def getFirstLine(self, text):

        # Grep data
        regexp_data = "'ss'>([^<].*)</p>"
        data_list = re.findall(regexp_data, text)    
        data = data_list[0] + " [" + str(self.getWidth()) + " x " + str(self.getHeight()) + "] "
        return data.encode("utf8")

    def getScriptureLine(self, text):

        # Grep data
        regexp_level_0 = "'sa'><i>(.*)\(</i>"
        level_0_list = re.findall(regexp_level_0, text)    
        if level_0_list == []:
            return ""
        level_0 = level_0_list[0]

        regexp_level_1 = "<a.*<i>(.*)</i></a><i>"
        level_1_list = re.findall(regexp_level_1, text)    
        if level_1_list == []:
            level_1 = ""
        level_1 = level_1_list[0]

        return level_0.encode("utf8")  + " - " + level_1.encode("utf8")

    def getComment(self, text):

        regexp_full_comment = "'sb'>(.*)"
        full_comment_list = re.findall(regexp_full_comment, text)
        if full_comment_list == []:
            return ""
        full_comment = full_comment_list[0]

        full_comment = re.sub("<([^>]*)>", " ", full_comment)

        return  full_comment.encode("utf8")