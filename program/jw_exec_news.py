"""
NEWS RELATED FUNCTIONS
"""

import jw_config
import jw_common

import re
import urllib

import xbmc
import xbmcgui
import xbmcplugin

# List of available news
def showNewsIndex():

	language    = jw_config.language
	url 		= jw_config.const[language]["news_index"] 
	html 		= jw_common.loadUrl(url)

	regexp_title = '<h3><a href="([^"]+)">([^<]+)</a></h3>'
	news_found = re.findall(regexp_title, html)

	regexp_images = "data-img-size-sm='([^']+)'"
	images = re.findall(regexp_images, html)

	count = 0
	for news in news_found:
		# Discard lateral news because is always OLD
		if  count == ( len(news_found)  - 1 )  :
			continue 

		title = jw_common.cleanUpText( news[1] ) 
		listItem = xbmcgui.ListItem( 
			label  			= title,
			thumbnailImage 	= images[count]
		)	
		params = {
			"content_type"  : "executable", 
			"mode" 			: "open_news_page", 
			"url"			: news[0]
		} 
		url = jw_config.plugin_name + '?' + urllib.urlencode(params)
		xbmcplugin.addDirectoryItem(
			handle		= jw_config.pluginPid, 
			url			= url, 
			listitem	= listItem, 
			isFolder	= True 
		)  
		count = count + 1
	
	xbmcplugin.endOfDirectory(handle=jw_config.pluginPid)


def showNewsPage(url):

	url = "http://www.jw.org" + url
	print "#################### JWORG #################"
	print url 
	print "#################### JWORG #################"
	html 		= jw_common.loadUrl(url)

	print "******************** JWORG *****************"
	print html
	print "******************** JWORG *****************"

	new = News()
	new.customInit(html);
	new.doModal();
	del new
	xbmc.executebuiltin('Action("back")')



# Window showing daily text

#get actioncodes from https://github.com/xbmc/xbmc/blob/master/xbmc/guilib/Key.h
ACTION_MOVE_UP 		= 3
ACTION_MOVE_DOWN 	= 4

class News(xbmcgui.WindowDialog):

	def __init__(self):
		if jw_config.emulating: xbmcgui.Window.__init__(self)

	def customInit(self, text):

		border = 50; # px relative to 1280/720 fixed grid resolution

		# width is always 1280, height is always 720.
		bg_image = jw_config.dir_media + "blank.png"
		self.ctrlBackgound = xbmcgui.ControlImage(
			0,0, 
			1280, 720, 
			bg_image
		)
		
		self.ctrlBackgound2 = xbmcgui.ControlImage(
			0,0, 
			1280, 90, 
			bg_image
		)
		
		self.ctrlTitle= xbmcgui.ControlTextBox(
			border, 0, 
			1280 - border *2, 90, 
			'font35_title', "0xFF0000FF"
		)
		self.ctrlText= xbmcgui.ControlTextBox(
            border, 20, 
            1280 - border *2, 3000, 
            'font30', "0xFF000000"
        )

		
		self.addControl (self.ctrlBackgound)
		self.addControl (self.ctrlText)
		self.addControl (self.ctrlBackgound2)
		self.addControl (self.ctrlTitle)
		
		self.ctrlTitle.setText( self.getTitle(text) )
		self.ctrlText.setText( self.getText(text) )
		

	def onAction(self, action):
		# print action.getButtonCode()
		# print action.getId()
		(x,y) =  self.ctrlText.getPosition()
		print (x,y)

		if action == ACTION_MOVE_UP:
			if y > 0:
				return
			y = y + 50;
			self.ctrlText.setPosition(x,y)
			return

		if action == ACTION_MOVE_DOWN:
			(x,y) =  self.ctrlText.getPosition()
			y = y - 50;
			self.ctrlText.setPosition(x,y)
			return

		self.close()

	# Grep news title
	def getTitle(self, text):

		regexp_header = "<header><h1>(.*)</h1>"
		headers = re.findall(regexp_header, text)
		return headers[0]

	def getText(self, text):
		regexp_pars = '<p id="p[0-9]+" class="p[0-9]+">([^<]+)</p>'
		pars = re.findall(regexp_pars, text)
		out = ""
		for par in pars:
			out = out + "\n\n" + par
		return out