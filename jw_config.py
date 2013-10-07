import xbmc
import xbmcgui
import xbmcplugin

import sys
import urlparse
import os

import jw_common

# key is english name, value is the name of the locale IN the locale
locale_2_lang = {
	"Italian"	: "Italiano",
	"Polish"	: "Polski",
	"Dutch"		: "Nederlands"
}

const = {
	"Italiano" 	: {
		"lang_code"					: "I",

		"video_path" 				: "http://www.jw.org/it/video",
		
		"bible_index_audio"			: "http://www.jw.org/it/pubblicazioni/bibbia/nwt/libri/",
		"bible_audio_json"  		: "http://www.jw.org/apps/I_TRGCHlZRQVNYVrXF?output=json&pub=bi12&fileformat=MP3&alllangs=0&langwritten=I",
		
		"music_index"				: "http://www.jw.org/it/pubblicazioni/musica-cantici/",
		"dramas_index"				: "http://www.jw.org/it/pubblicazioni/drammi-biblici-audio/",
		"dramatic_reading_index"	: "http://www.jw.org/it/pubblicazioni/brani-biblici-recitati/",
		
		"magazine_index"			: "http://www.jw.org/it/pubblicazioni/riviste/",
		'has_simplified_edition'	: False,

		'daily_text_json'			: "http://wol.jw.org/wol/dt/r6/lp-i",
		"date_format"				: "%d/%m/%Y",
		"news_index"				: "http://www.jw.org/it/news/",

 	},
	"English" 	: {
		"lang_code"					: "E",
		"video_path" 				: "http://www.jw.org/en/videos",
		
		"bible_index_audio"			: "http://www.jw.org/en/publications/bible/nwt/books/" ,
		"bible_audio_json"  		: "http://www.jw.org/apps/E_TRGCHlZRQVNYVrXF?output=json&pub=bi12&fileformat=MP3&alllangs=0&langwritten=E",
		
		"music_index"				: "http://www.jw.org/en/publications/music-songs/",
		"dramas_index"				: "http://www.jw.org/en/publications/audio-bible-dramas/",
		"dramatic_reading_index"	: "http://www.jw.org/en/publications/dramatic-bible-readings/",

		"magazine_index"			: "http://www.jw.org/en/publications/magazines/",
		'has_simplified_edition'	: True,

		'daily_text_json'			: "http://wol.jw.org/wol/dt/r1/lp-e",
		"date_format"				: "%Y-%m-%d",
		"news_index"				: "http://www.jw.org/en/news/",
	},
	"Polski" 	: {
		"lang_code"					: "P",
		"video_path" 				: "http://www.jw.org/pl/filmy/",
		
		"bible_index_audio"			: "http://www.jw.org/pl/publikacje/biblia/nwt/ksi%C4%99gi-biblijne/" , 
		"bible_audio_json"  		: "http://www.jw.org/apps/TRGCHlZRQVNYVrXF?output=json&pub=bi12&fileformat=MP3&alllangs=0&langwritten=P&txtCMSLang=P",
		
		"music_index"				: "http://www.jw.org/pl/publikacje/muzyka-pie%C5%9Bni/",
		"dramas_index"				: "http://www.jw.org/pl/publikacje/s%C5%82uchowiska-biblijne/",
		"dramatic_reading_index"	: "http://www.jw.org/pl/publikacje/adaptacje-d%C5%BAwi%C4%99kowe-biblii/",
		
		"magazine_index"			: "http://www.jw.org/pl/publikacje/czasopisma/",
		'has_simplified_edition'	: False,

		'daily_text_json'			: "http://wol.jw.org/wol/dt/r12/lp-p",
		"date_format"				: "%d-%m-%Y",
		"news_index"				: "http://www.jw.org/pl/wiadomo%C5%9Bci/"
	},	
	"Nederlands" : {
		"lang_code"					: "O",
		"video_path" 				: "http://www.jw.org/nl/videos/",

		"bible_index_audio"			: "http://www.jw.org/nl/publicaties/bijbel/nwt/boeken/" , 
		"bible_audio_json"  		: "http://www.jw.org/apps/TRGCHlZRQVNYVrXF?output=json&pub=bi12&fileformat=MP3&alllangs=0&langwritten=O&txtCMSLang=O", #last 2 are letters 'o' not zero
		
		"music_index"				: "http://www.jw.org/nl/publicaties/muziek-liederen/",
		"dramas_index"				: "http://www.jw.org/nl/publicaties/audio-bijbel-dramas/",
		"dramatic_reading_index"	: "http://www.jw.org/nl/publicaties/bijbelse-hoorspelen/",
		
		"magazine_index"			: "http://www.jw.org/nl/publicaties/tijdschriften/",
		'has_simplified_edition'	: False,

		'daily_text_json'			: "http://wol.jw.org/wol/dt/r18/lp-o",
		"date_format"				: "%d-%m-%Y",
		"news_index"				: "http://www.jw.org/nl/nieuws/"
	},	
}


plugin_name 	= sys.argv[0]   # plugin://plugin.video.jworg/
pluginPid   	= int(sys.argv[1])
plugin_params 	= urlparse.parse_qs((sys.argv[2])[1:])
skin_used 		= xbmc.getSkinDir()
dir_media		= os.path.dirname(__file__) + os.sep + "resources" + os.sep + "media" + os.sep

try: 
	emulating = xbmcgui.Emulating
except: 
	emulating = False

try:
	import StorageServer
except:
	from resources.lib import storageserverdummy as StorageServer
	 
cache 			= StorageServer.StorageServer(plugin_name, 24)  # 2 hour cache
audio_sorting 	= str(int(xbmcplugin.getSetting(pluginPid, "audio_sorting")) + 1)
video_sorting 	= str(int(xbmcplugin.getSetting(pluginPid, "video_sorting")) + 1)

# if language is set, it used a localized language name, like "Italiano" or "Polski"
language		= xbmcplugin.getSetting(pluginPid, "language")

# if not set, language will be read from system, where it uses english language name
# if it's one of supported language, I got localized name to adhere to addon language setting 
# availables values ( Italiano, English, Polski, ... )

if language == "":
	actual_locale = xbmc.getLanguage()
	#print "Locale detected " + actual_locale
	if actual_locale in locale_2_lang :
		language = locale_2_lang[actual_locale]
	else :
		language = "English"

	#print "Language setted " + language