# -*- coding: UTF-8 -*-
"""
SIGN LANGUAGE VIDEO RELATED FUNCTIONS
"""

import xbmcplugin
import BeautifulSoup 

import jw_common
import jw_config

# show available video categories
def showVideoFilter():
	import re

	doc = ['<html><head><title>Page title</title></head>',
		'<body><p id="firstpara" align="center">This is paragraph <b>one</b>.',
		'<p id="secondpara" align="blah">This is paragraph <b>two</b>.',
		'</html>']
	soup = BeautifulSoup(''.join(doc))

	print soup.prettify()

	language 	= jw_config.language;
	url 		= jw_common.getUrl(language) + jw_config.const[language]["video_path"] 
	print url;

	xbmcplugin.endOfDirectory(handle=jw_config.plugin_pid);
