# -*- coding: UTF-8 -*-

# for utf-8 see http://www.python.org/dev/peps/pep-0263/

import xbmc
import xbmcaddon
import xbmcplugin
import xbmcgui
import sys
import re

import urllib
import urllib2
import urlparse
import json
import HTMLParser

"""
VIDEO RELATED FUNCTION
"""

# show available video categories
def showVideoFilter():
	global pluginPid, plugin
	settings_l18n_code = getVideoPathByLanguage();	
	url = "http://www.jw.org/"+ settings_l18n_code
	html = loadUrl(url)
	# print "JWORG html dump" + html
	regexp_video_filters = '<option data-priority.* value="([^"]+)">([^<]+)</option>'
	filters = re.findall(regexp_video_filters, html) 
	# print "JWORG filters:"
	# print filters
	# Output video filter list
	for video_filter in filters:
		# print "JWORG filtro trovato:"
		# print video_filter
		title = video_filter[1].replace("&amp;","&")
		listItem = xbmcgui.ListItem( title )	
		params = {"content_type" : "video", "mode": "open_video_page", "start" : 0, "video_filter" : video_filter[0]} 
		url = sys.argv[0] + '?' + urllib.urlencode(params)
		xbmcplugin.addDirectoryItem(handle=pluginPid, url=url, listitem=listItem, isFolder=True )  
	
	xbmcplugin.endOfDirectory(handle=pluginPid)
	

# show available video pages
def showVideoIndex(start, video_filter):
	global pluginPid, plugin

	settings_l18n_code = getVideoPathByLanguage();

	url = "http://www.jw.org/"+ settings_l18n_code + "/?start=" + str(start) + "&videoFilter=" + video_filter
	print "JWORG ShowVideoIndex url: " + url

	html = loadUrl (url)

	# Grep video titles
	regexp_video_title = 'data-onpagetitle="([^"]+)"'
	videos = re.findall(regexp_video_title, html)  

	# Grep poster of video
	regexp_video_poster = 'data-img-size-md=["\']([^"\']+)["\']'
	posters = re.findall(regexp_video_poster, html)

	# Grep url of json wich contain data on different version of the video [240,360, etc..]
	# regexp_video_json = '^data-jsonurl="([^"]+)"';
	regexp_video_json = '.*[^"] data-jsonurl="([^"]+)".*';
	video_json = re.findall(regexp_video_json, html)

	# Grep video pages links [0, 1, 2, etc..]
	regexp_video_next_page = '<a class="iconNext.*start=([0-9]+).*title="([^""]+)"'
	next_link = re.findall(regexp_video_next_page, html)

	count = 0
	# Output video list 
	for title in videos:
		listItem = xbmcgui.ListItem(
			label=title, 
			thumbnailImage= posters[count]
		)

		print "JWORG title: " + title
		json_url = video_json[count]
		print "JWORG json_url: " + json_url
		params = {"content_type" : "video", "mode" : "open_json_video", "json_url": json_url} 
		url = sys.argv[0] + '?' + urllib.urlencode(params)
		xbmcplugin.addDirectoryItem(
			handle=pluginPid, 
			url=url, 
			listitem=listItem, 
			isFolder=True 
		)  
		count = count + 1

	# Output next page link
	try: 
		next_start =  next_link[0][0]
		title = plugin.getLocalizedString(30001);
		listItem = xbmcgui.ListItem(title)
		params = {"content_type" : "video", "mode": "open_video_page", "start" : next_start, "video_filter" : video_filter} 
		url = sys.argv[0] + '?' + urllib.urlencode(params)
		xbmcplugin.addDirectoryItem(handle=pluginPid, url=url, listitem=listItem, isFolder=True )  
	except:
		pass

	xbmcplugin.endOfDirectory(handle=pluginPid)

# show available resolutions for a video (ed eventually other related titles, like interviews, etc.)	
def showVideoJsonUrl(json_url):
	global plugin;

	json_url = "http://www.jw.org" + json_url
	print "JWORG video json url: " + json_url
	#  /apps/I_TRGCHlZRQVNYVrXF?fileformat=mp4&output=json&pub=ivfe&langwritten=I&alllangs=1
	json = loadJsonFromUrl(json_url)

	if json is None :
		string = plugin.getLocalizedString(30008) + " ";
		xbmcgui.Dialog().ok("jworg browser", string)
		return

	language_code = None;
	video_lang_code =getVideoLangCodeByLanguage() 
	print "JWORG video lang code " + video_lang_code
	for language in  json["languages"]:
		locale =  json["languages"][language]["locale"]
		if locale == video_lang_code:
			language_code = language
			break


	print "JWORG language_code " + language_code

	#adesso ho in locale una lettera tipo 'I' per l'italiano per accedere all'url del file
	if language_code == None:
		string = plugin.getLocalizedString(30006) + " ";
		xbmcgui.Dialog().ok("jworg browser", string)
		return

	options = []
	mp4_to_play = []
	for mp4 in json["files"][language_code]["MP4"]:
		url = mp4["file"]["url"]
		res = mp4["label"]
		title = mp4["title"]
		title = "[" + res + "] - " + title
		# print mp4
		print url
		mp4_to_play.append(url);
		options.append(title.encode('utf8'))
		print title.encode('utf8')

	# Scelta formato e filmato da eseguire
	dia = xbmcgui.Dialog()
	string = plugin.getLocalizedString(30007) + " ";
	selected = dia.select(string, options)
	if selected != -1 :
		print "JWORG I'll play " + mp4_to_play[selected]
		xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(mp4_to_play[selected])


"""
AUDIO RELATED FUNCTION
"""


"""
UTILITY
"""
def loadUrl (url):
	response = urllib2.urlopen(url)
	html = response.read()
	return html	

def loadJsonFromUrl (url):
	data = None
	try:
		response = urllib2.urlopen(url)
		data = json.load(response)
	except:
		pass
	return data

def getVideoPathByLanguage ():
	global language;
	locale_codes = { "Italiano": "it/video", "English" : "en/videos" }
	return locale_codes[language]

def getVideoLangCodeByLanguage ():
	global language;
	locale_codes = { "Italiano": "it", "English" : "en" }
	return locale_codes[language]


"""
START
"""

# Gloal used in all xbmc 
plugin       = xbmcaddon.Addon("plugin.video.jworg")
pluginPid    = int(sys.argv[1])
language     = xbmcplugin.getSetting(pluginPid, "language")
print "JWORG language: " + language
if language == "":
	language = "English"

# Debug; call arguments
params 		 = urlparse.parse_qs((sys.argv[2])[1:])
print "JWORG argomenti lancio: " 
print sys.argv
print params

content_type = "video"
try:
	content_type = params["content_type"][0]
except:
	pass

mode = None
try:	
	mode = params["mode"][0]
except:
	pass

start = None
try:
	start = params["start"][0]        
except:
    pass

video_filter = None
try:
	video_filter = params["video_filter"][0]	#Note: video_filter can be 'none', and it's a valid filter for jw.org !
except:
	pass

# Call router
if content_type == "video" and mode is None :
	showVideoFilter();

if content_type == "video" and mode == "open_video_page" and start is not None:
	showVideoIndex(start, video_filter);

if content_type == "video" and mode == "open_json_video":
	json_url = params["json_url"][0]
	showVideoJsonUrl(json_url);

