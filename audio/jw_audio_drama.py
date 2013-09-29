"""
AUDIO DRAMAS RELATED FUNCTIONS
"""

import jw_config
import jw_common

import re
import urllib

import xbmcgui
import xbmcplugin


# List of dramas
def showDramaIndex(start):
	
	language 		= jw_config.language
	drama_index_url = jw_config.const[language]["dramas_index"] + "?start=" + start + "&sortBy=" + jw_config.audio_sorting
	html 			= jw_common.loadUrl(drama_index_url) 
	
	# Grep drama titles
	regexp_dramas_titles = '"pubAdTitleBlock">([^<]+)<'
	drama_titles = re.findall(regexp_dramas_titles, html)  	
	
	# Grep drama json
	regexp_drama_json = 'class="jsDownload" data-jsonurl="([^"]+MP3[^"]+)".*'
	drama_json = re.findall(regexp_drama_json, html)

	# Grep drama  image - [^\'.]+ discards ".prd_md" duplicated images
	regexp_drama_thumb = 'data-img-size-md=\'(http://assets.jw.org/assets/[^\'.]+_md\.jpg)\''
	drama_thumb = re.findall(regexp_drama_thumb, html)

	drama_num = 0
	for drama in drama_titles:
		listItem = xbmcgui.ListItem(
			label 			= drama_titles[drama_num],
			thumbnailImage  = drama_thumb[drama_num]
		)	
		params = {
			"content_type"  : "audio", 
			"mode" 			: "open_drama_json",
			"json_url" 		: drama_json[drama_num] 
		}
		url = jw_config.plugin_name + '?' + urllib.urlencode(params)	
		xbmcplugin.addDirectoryItem(
			handle		= jw_config.pluginPid, 
			url 		= url, 
			listitem 	= listItem, 
			isFolder	= True 
		)  
		drama_num = drama_num + 1

	jw_common.setNextPageLink(html, "open_drama_index", "audio")

	xbmcplugin.endOfDirectory(handle=jw_config.pluginPid)
	jw_common.setThumbnailView()


# Track list
def showDramaJson(json_url):

	language 		= jw_config.language
	language_code 	= jw_config.const[language]["lang_code"]
	json_url 		= "http://www.jw.org" + json_url
	json 			= jw_common.loadJsonFromUrl(json_url)
	
	for mp3 in json["files"][language_code]["MP3"]:
		url 	= mp3["file"]["url"]
		title 	= mp3["title"]
		title 	= jw_common.cleanUpText(title)

		# Skip 'zip' files
		if mp3["mimetype"] != "audio/mpeg":
			continue;

		listItem = xbmcgui.ListItem(label=title)
		listItem.setInfo(
			type 		= 'Music', 
			infoLabels  = {'Title': title }
		)

		xbmcplugin.addDirectoryItem(
			handle 		= jw_config.pluginPid, 
			url 		= url, 
			listitem 	= listItem, 
			isFolder 	= False
		)  

	xbmcplugin.endOfDirectory(handle=jw_config.pluginPid)