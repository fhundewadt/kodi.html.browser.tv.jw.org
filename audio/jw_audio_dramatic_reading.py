"""
DRAMATICA BIBLE READING RELATED FUNCTIONS
"""
import jw_config
import jw_common

import re
import urllib

import xbmcplugin
import xbmcgui


# List of reading
def showDramaticReadingIndex(start):
	
	language 			= jw_config.language
	reading_index_url 	= jw_config.const[language]["dramatic_reading_index"] + "?start=" + start
	html 				= jw_common.loadUrl(reading_index_url) 
	
	# Grep reading titles
	regexp_reading_titles = '"pubAdTitleBlock">([^<]+)<'
	reading_title = re.findall(regexp_reading_titles, html)  	
	
	# Grep reading json
	regexp_reading_json = 'class="jsDownload" data-jsonurl="([^"]+MP3[^"]+)".*'
	reading_json = re.findall(regexp_reading_json, html)

	# Grep reading images - [^\'.]+ discards ".prd_md" duplicated images
	regexp_reading_thumb = 'data-img-size-md=\'(http://assets.jw.org/assets/[^\'.]+_md\.jpg)\''
	reading_thumb = re.findall(regexp_reading_thumb, html)

	reading_num = 0
	for reading in reading_title:
		listItem = xbmcgui.ListItem(
			label 			= reading_title[reading_num], 
			thumbnailImage  = reading_thumb[reading_num]
		)	
		params = {
			"content_type"  : "audio", 
			"mode" 			: "open_dramatic_reading_json", 
			"json_url" 		: reading_json[reading_num] 
		}
		url = jw_config.plugin_name + '?' + urllib.urlencode(params)	
		xbmcplugin.addDirectoryItem(
			handle		= jw_config.pluginPid, 
			url 		= url, 
			listitem 	= listItem, 
			isFolder	= True 
		)  
		reading_num = reading_num + 1

	jw_common.setNextPageLink(html, "open_dramatic_reading_index", "audio")

	xbmcplugin.endOfDirectory(handle=jw_config.pluginPid)
	jw_common.setThumbnailView()


# Track list
def showDramaticReadingJson(json_url):

	language 	= jw_config.language
	json_url 	= "http://www.jw.org" + json_url
	json 		= jw_common.loadJsonFromUrl(json_url)

	language_code = jw_config.const[language]["lang_code"]
	
	for mp3 in json["files"][language_code]["MP3"]:
		url 	= mp3["file"]["url"]
		title 	= jw_common.cleanUpText(mp3["title"])

		# Skip 'zip' files
		if mp3["mimetype"] != "audio/mpeg":
			continue;

		listItem = xbmcgui.ListItem(label=title)
		listItem.setInfo(
			type 		= 'Music', 
			infoLabels  = {'Title': mp3["title"] }
		)

		xbmcplugin.addDirectoryItem(
			handle 		= jw_config.pluginPid, 
			url 		= url, 
			listitem 	= listItem, 
			isFolder 	= False
		)  

	xbmcplugin.endOfDirectory(handle=jw_config.pluginPid)