"""
AUDIO BIBLE RELATED FUNCTIONSS
"""
import xbmc
import xbmcgui
import xbmcplugin

import urllib
import re

import jw_config
import jw_common

# List of albums
def showMusicIndex(start):
	
	language 		= jw_config.language
	music_index_url = jw_config.const[language]["music_index"] + "?start=" + start
	html 			= jw_common.loadUrl(music_index_url) 
	
	# Grep compilation titles
	regexp_music_title = '"pubAdTitleBlock">([^<]+)<'
	music_title = re.findall(regexp_music_title, html)  	

	# Grep music json
	regexp_music_json = 'class="jsDownload" data-jsonurl="([^"]+MP3[^"]+)".*'
	music_json = re.findall(regexp_music_json, html)

	# Grep compilation image - [A-Z]+ discards ".prd_md" duplicated images
	regexp_music_thumb = 'data-img-size-md=["\']([^"\']+[A-Z]+_md\.jpg)["\']'
	music_thumb = re.findall(regexp_music_thumb, html)

	album_num = 0
	for album in music_title:
		listItem = xbmcgui.ListItem(
			label 			= music_title[album_num], 
			thumbnailImage  = music_thumb[album_num]
		)	
		params = {
			"content_type"  : "audio", 
			"mode" 			: "open_music_json", 
			"json_url" 		: music_json[album_num] 
		}
		url = jw_config.plugin_name + '?' + urllib.urlencode(params)	
		xbmcplugin.addDirectoryItem(
			handle		= jw_config.pluginPid, 
			url 		= url, 
			listitem 	= listItem, 
			isFolder	= True 
		)  
		album_num = album_num + 1

	jw_common.setNextPageLink(html, "open_music_index", "audio")

	xbmcplugin.endOfDirectory(handle=jw_config.pluginPid)
	if jw_config.skin_used == 'skin.confluence': 
		xbmc.executebuiltin('Container.SetViewMode(500)') 


# Track list
def showMusicJson(json_url):

	language 	= jw_config.language
	json_url 	= "http://www.jw.org" + json_url
	json 		= jw_common.loadJsonFromUrl(json_url)

	language_code = jw_config.const[language]["lang_code"]
	
	for mp3 in json["files"][language_code]["MP3"]:
		url 	= mp3["file"]["url"]
		title 	= mp3["title"]

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