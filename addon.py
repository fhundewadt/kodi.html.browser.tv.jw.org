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

"""
FUNCTION PRINCIPALI
"""

# elenca le pagine disponibili
def showVideoIndex(start):
	global pluginPid, plugin

	settings_l18n_code = getVideoByLanguageCode();

	url = "http://www.jw.org/"+ settings_l18n_code + "/?start=" + str(start)
	print "JWORG ShowVideoIndex url: " + url

	html = loadUrl (url)

	# Recupero link delle pagine

	regexp_video_pages = '<a href="[^"]+=([0-9]+)" class="pageNum">([0-9]+)</a>'
	other_pages = re.findall(regexp_video_pages, html)
	
	# print other_pages
	other_pages =  list(set(other_pages))
	other_pages.sort()

	# Recupero titoli dei video
	# C'è una sola regexp quindi è una semplice lista, un array non associativo
	regexp_video_title = 'data-onpagetitle="([^"]+)"'
	videos = re.findall(regexp_video_title, html) 

	# Recupero immagine "locandina" del video
	regexp_video_poster = '<img src=["\'](assets[^"\']+)["\']'
	posters = re.findall(regexp_video_poster, html)

	regexp_video_json = 'data-jsonurl="([^"]+)"';
	video_json = re.findall(regexp_video_json, html)

	count = 0
	for title in videos:
		# print "JWORG title n. " + str(count) + ": " + title + " image at: " + posters[count]
		listItem = xbmcgui.ListItem(
			label=title, 
			thumbnailImage= "http://www.jw.org/" + posters[count]
		)

		params = {"content_type" : "video", "mode" : "open_json_video", "json_url": video_json[count]} 
		url = sys.argv[0] + '?' + urllib.urlencode(params)
		xbmcplugin.addDirectoryItem(
			handle=pluginPid, 
			url=url, 
			listitem=listItem, 
			isFolder=True 
		)  
		count = count + 1

	# Link alle pagine
	for page in other_pages:
		next_start =  page[0] 
		if next_start <= start:
			continue;
		pagina = page[1] 
		l18n_gotopage = plugin.getLocalizedString(30001) + " ";
		title = l18n_gotopage + str(page[1])
		print "JWORG title " + title
		listItem = xbmcgui.ListItem(title)
		params = {"content_type" : "video", "start" : next_start} 
		url = sys.argv[0] + '?' + urllib.urlencode(params)
		print "JWORG list url " + url
		xbmcplugin.addDirectoryItem(handle=pluginPid, url=url, listitem=listItem, isFolder=True )  
		# appena trovo il link alla pagina successiva esco
		break;

	xbmcplugin.endOfDirectory(handle=pluginPid)
	
	
def showVideoJsonUrl(json_url):
	global plugin;

	print "JWORG video json url: " + json_url
	#  /apps/I_TRGCHlZRQVNYVrXF?fileformat=mp4&output=json&pub=ivfe&langwritten=I&alllangs=1
	json = loadJsonFromUrl("http://www.jw.org" + json_url)

	if json is None :
		string = plugin.getLocalizedString(30008) + " ";
		xbmcgui.Dialog().ok("jworg browser", string)
		return

	language_code = None;
	for language in  json["languages"]:
		locale =  json["languages"][language]["locale"]
		if locale == "it":
			language_code = language
			break

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

def getVideoByLanguageCode ():
	global language;
	locale_codes = { "Italiano": "it/video", "English" : "en/videos" }
	return locale_codes[language]

"""
START
"""

# Usato in tutte le chiamate ad addDirectory
plugin       = xbmcaddon.Addon("plugin.video.jworg")
pluginPid    = int(sys.argv[1])
language     = xbmcplugin.getSetting(pluginPid, "language")
print "JWORG language: " + language
if language == "":
	language = "English"

# Stampo per debug gli argomenti della chiamata
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

start = 0
try:
	start = params["start"][0]        
except:
    pass

#lingua

if content_type == "video" and mode is None:
	showVideoIndex(start);

if content_type == "video" and mode == "open_json_video":
	json_url = params["json_url"][0]
	showVideoJsonUrl(json_url);


