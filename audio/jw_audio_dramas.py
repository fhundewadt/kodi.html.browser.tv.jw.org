"""
AUDIO DRAMAS RELATED FUNCTION
"""

import jw_config
import jw_load

import re
import urllib

import xbmcgui
import xbmcplugin
import xbmc


# List of DRAMAS
def showDramaIndex(start):
	
	language 		= jw_config.language
	music_index_url = jw_config.const[language]["dramas_index"] + "?start=" + start
	html 			= jw_load.loadUrl(music_index_url) 
	
	# Grep drama titles
	regexp_dramas_titles = '"pubAdTitleBlock">([^<]+)<'
	drama_titles = re.findall(regexp_dramas_titles, html)  	
	
	# Grep drama json
	regexp_drama_json = 'class="jsDownload" data-jsonurl="([^"]+MP3[^"]+)".*'
	drama_json = re.findall(regexp_drama_json, html)

	# Grep drama  image - [^\'.]+ discards ".prd_md" duplicated images
	regexp_drama_thumb = 'data-img-size-md=\'(http://assets.jw.org/assets/[^\'.]+_md\.jpg)\''
	drama_thumb = re.findall(regexp_drama_thumb, html)

	book_num = 0
	for book in drama_titles:
		listItem = xbmcgui.ListItem(
			label 			= drama_titles[book_num],
			thumbnailImage  = drama_thumb[book_num]
		)	
		params = {
			"content_type"  : "audio", 
			"mode" 			: "open_drama_json",
			"json_url" 		: drama_json[book_num] 
		}
		url = jw_config.plugin_name + '?' + urllib.urlencode(params)	
		xbmcplugin.addDirectoryItem(
			handle		= jw_config.pluginPid, 
			url 		= url, 
			listitem 	= listItem, 
			isFolder	= True 
		)  
		book_num = book_num + 1

	# Grep video pages "NEXT" link
	regexp_video_next_page = '<a class="iconNext.*start=([0-9]+).*title="([^""]+)"'
	next_link = re.findall(regexp_video_next_page, html)

	# Output next page link
	try: 
		next_start  = next_link[0][0]
		title 		= jw_config.t(30001);	
		listItem 	= xbmcgui.ListItem(title)
		params 		= {
			"content_type" 	: "audio", 
			"mode" 			: "open_drama_index", 
			"start" 		: next_start 
		} 
		url = jw_config.plugin_name + '?' + urllib.urlencode(params)
		xbmcplugin.addDirectoryItem(
			handle		= jw_config.pluginPid, 
			url			= url, 
			listitem	= listItem, 
			isFolder	= True 
		)  
	except:
		pass

	xbmcplugin.endOfDirectory(handle=jw_config.pluginPid)
	if jw_config.skin_used == 'skin.confluence': 
		xbmc.executebuiltin('Container.SetViewMode(500)') 


# Track list
def showDramaJson(json_url):

	language 		= jw_config.language
	language_code 	= jw_config.const[language]["lang_code"]
	json_url 		= "http://www.jw.org" + json_url
	json 			= jw_load.loadJsonFromUrl(json_url)
	
	for mp3 in json["files"][language_code]["MP3"]:
		url 	= mp3["file"]["url"]
		title 	= mp3["title"]
		title 	= title.replace("&#039;", "'")

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