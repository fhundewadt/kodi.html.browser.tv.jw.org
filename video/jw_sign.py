# -*- coding: UTF-8 -*-
"""
SIGN LANGUAGE VIDEO RELATED FUNCTIONS
"""

import xbmcplugin
import xbmcgui

from BeautifulSoup import BeautifulSoup 
import urllib

import jw_common
import jw_config

# show available video categories
def showVideoFilter():
	import re

	language 	= jw_config.language;
	url 		= jw_config.main_url  + jw_config.const[language]["sign_index"] 
	if url is False :
		print "No sign language support for language " + language
		xbmcplugin.endOfDirectory(handle=jw_config.plugin_pid)
		return;
		
	print  "JWORG sign url: " + url

	html 		= jw_common.loadUrl(url)

 	

	soup = BeautifulSoup(html)

	# print soup.prettify()
	boxes = soup.findAll('div',{"class":"box"})

	for box in boxes :
		box_content = box.findAll('div',{'class':'boxcontent'})
		for content in box_content :

			content_divs = content.findAll('div');
			img_src 		= content_divs[0].findAll('img')[0].get("src")
			category_link 	= content_divs[1].find('a').get('href')
			category_name	= content_divs[1].find('a').contents[0].encode("utf-8")

			listItem = xbmcgui.ListItem(
				label 			= category_name, 
				thumbnailImage 	= img_src
			)

			params = { 
				"content_type" 	: "video", 
				"mode" 			: "open_sign_video_category", 
				"url"			: category_link,
				"thumb" 		: img_src
			} 

			url = jw_config.plugin_name + '?' + urllib.urlencode(params)
			xbmcplugin.addDirectoryItem(
				handle	 = jw_config.plugin_pid, 
				url 	 = category_link, 
				listitem =listItem, 
				isFolder =True 
			)  

	xbmcplugin.endOfDirectory(handle=jw_config.plugin_pid)
