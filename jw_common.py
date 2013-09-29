import re
import urllib
import urllib2
import json

import jw_config

import xbmcgui
import xbmcplugin

# Grep "NEXT" link and add to current directory
# param_name and param_value is used to pass addition param when adding directory item
def setNextPageLink(html, mode, type, param_name = None, param_value = None):

	regexp_video_next_page = '<a class="iconNext.*start=([0-9]+).*title="([^""]+)"'
	next_link = re.findall(regexp_video_next_page, html)

	if next_link == []:
		return 

	next_start  = next_link[0][0]
	title 		= jw_config.t(30001);	
	listItem 	= xbmcgui.ListItem(title)
	params 		= {
		"content_type" 	: type, 
		"mode" 			: mode, 
		"start" 		: next_start 
	} 
	if param_name is not None :
		params[param_name] = param_value

	url = jw_config.plugin_name + '?' + urllib.urlencode(params)

	xbmcplugin.addDirectoryItem(
		handle		= jw_config.pluginPid, 
		url			= url, 
		listitem	= listItem, 
		isFolder	= True 
	)  

def loadNotCachedUrl(url):
	response = urllib2.urlopen (url)
	html = response.read()
	return html		

def loadUrl (url):
	html = jw_config.cache.cacheFunction(loadNotCachedUrl, url)
	return html	

def loadNotCachedJsonFromUrl(url):
	data = None
	try:
		response = urllib2.urlopen(url)
		data = json.load(response)
	except:
		pass
	return data

def loadJsonFromUrl (url):
	data = jw_config.cache.cacheFunction(loadNotCachedJsonFromUrl, url)	
	return data




