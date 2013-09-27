# -*- coding: UTF-8 -*-

# for utf-8 see http://www.python.org/dev/peps/pep-0263/

import xbmcplugin

import jw_config

from video import jw_video

from audio import jw_audio_index
from audio import jw_audio_bible
from audio import jw_audio_music

from program import jw_exec_index
from program import jw_exec_daily_text

"""
START
"""
# call arguments
params 		 = jw_config.plugin_params

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


"""
Call router
"""
if content_type == "video" and mode is None :
	jw_video.showVideoFilter()

if content_type == "video" and mode == "open_video_page" and start is not None:
	video_filter = params["video_filter"][0]	#Note: video_filter can be 'none', and it's a valid filter for jw.org !
	jw_video.showVideoIndex(start, video_filter)

if content_type == "video" and mode == "open_json_video":
	json_url 	= params["json_url"][0]
	thumb 		= params["thumb"][0]
	jw_video.showVideoJsonUrl(json_url, thumb)

if content_type == "audio" and mode is None :
	jw_audio_index.showAudioTypeIndex()

if content_type == "audio" and mode == "open_bible_index" :
	jw_audio_bible.showAudioBibleIndex()

if content_type == "audio" and mode == "open_bible_book_index"  :
	book_num = params["book_num"][0]
	jw_audio_bible.showAudioBibleBookJson(book_num)

if content_type == "audio" and mode == "open_music_index"  and start is not None: 
	jw_audio_music.showMusicIndex( start);

if content_type == "audio" and mode == "open_music_json" : 
	json_url = params["json_url"][0]
	jw_audio_music.showMusicJsonUrl(json_url);

if content_type == "executable" and mode is None : 
	jw_exec_index.showExecIndex();

if content_type == "executable" and mode == "open_daily_text" : 
	date = params["date"][0]
	jw_exec_daily_text.showDailyText(date);	