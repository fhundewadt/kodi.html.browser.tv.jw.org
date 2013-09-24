"""
EXECUTABLE RELATED FUNCTION
"""
import xbmcgui
import xbmcplugin

import jw_config
import jw_load

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

	print "JWORG showDailyText " + date
	json_url = jw_config.const[language]["daily_text_json"] + "/" + date
	print "JWORG daily text json " + json_url
	json = jw_load.loadJsonFromUrl(json_url)
	print json

	mydisplay = MyClass()
	mydisplay .doModal()
	del mydisplay



#get actioncodes from https://github.com/xbmc/xbmc/blob/master/xbmc/guilib/Key.h
ACTION_PREVIOUS_MENU = 10
 
class MyClass(xbmcgui.Window):
  def __init__(self):
    self.strActionInfo = xbmcgui.ControlLabel(100, 120, 200, 200, '', 'font13', '0xFFFF00FF')
    self.addControl(self.strActionInfo)
    self.strActionInfo.setLabel('Push BACK to quit')
    self.button0 = xbmcgui.ControlButton(250, 100, 80, 30, "HELLO")
    self.addControl(self.button0)
    self.button1 = xbmcgui.ControlButton(250, 200, 80, 30, "HELLO2")
    self.addControl(self.button1)
    self.button2 = xbmcgui.ControlButton(450, 200, 80, 30, "HELLO3")
    self.addControl(self.button2)
    self.setFocus(self.button0)
    self.button0.controlDown(self.button1)
    self.button1.controlUp(self.button0)
    self.button1.controlRight(self.button2)
    self.button2.controlLeft(self.button1)
 
  def onAction(self, action):
    if action == ACTION_PREVIOUS_MENU:
      self.close()
 
  def onControl(self, control):
    if control == self.button0:
      self.message('you pushed the 1st button')
    if control == self.button1:
      self.message('you pushed the 2nd button')
    if control == self.button2:
      self.message('you pushed the 3rd button')
 
  def message(self, message):
    dialog = xbmcgui.Dialog()
    dialog.ok(" My message title", message)
 
mydisplay = MyClass()
mydisplay .doModal()
del mydisplay