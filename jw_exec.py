"""
EXECUTABLE RELATED FUNCTION
"""
import xbmcgui
import xbmcplugin

import jw_config

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
def showDailyText(date):

	print "JWPRG showDailyText " + date