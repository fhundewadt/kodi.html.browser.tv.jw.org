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

	language 	= jw_config.language;
	url 		= jw_config.main_url  + jw_config.const[language]["sign_index"] 
	if url is False :
		print "No sign language support for language " + language
		xbmcplugin.endOfDirectory(handle=jw_config.plugin_pid)
		return;

	html 	= jw_common.loadUrl(url)
	soup 	= BeautifulSoup(html)

	# print soup.prettify()
	boxes 	= soup.findAll('div',{"class":"box"})

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
				url 	 = url, 
				listitem = listItem, 
				isFolder = True 
			)  

	xbmcplugin.endOfDirectory(handle=jw_config.plugin_pid)


def showVideoCategory(category_url, thumb) :

	html 	= jw_common.loadUrl(category_url)
	soup 	= BeautifulSoup(html)

	pub_title = soup.findAll('tr', {'class' : "pubTitle"})

	pub_title_found = len(pub_title)
	
	if  pub_title_found > 1 :

		pub_title_index = -1;
		for title in pub_title :

			issue_title_cell = title.findAll('th')[0]
			
			issue_title = issue_title_cell.find('em').contents[0].encode("utf-8")
			issue_title = issue_title + issue_title_cell.contents[1].encode("utf-8")
			issue_title = jw_common.cleanUpText(issue_title);

			pub_title_index = pub_title_index + 1

			listItem = xbmcgui.ListItem(
				label 			= issue_title, 
				thumbnailImage 	= thumb
			)

			params = { 
				"content_type" 		: "video", 
				"mode" 				: "open_sign_video_category_with_specific_issue", 
				"url"				: category_url,
				"thumb" 			: thumb,
				"pub_title_index"	: pub_title_index
			} 

			url = jw_config.plugin_name + '?' + urllib.urlencode(params)
			xbmcplugin.addDirectoryItem(
				handle	 = jw_config.plugin_pid, 
				url 	 = url, 
				listitem = listItem, 
				isFolder = True 
			)  

		xbmcplugin.endOfDirectory(handle=jw_config.plugin_pid)
		return

	xbmcplugin.endOfDirectory(handle=jw_config.plugin_pid)



# This specific version is for watchtower page, which has more than one pub per page
# The previous folder has already showed the list of issue of this category of publication
# Here I got the index ( zero based). So I'll browser entire table, and discard
# all of chapters not related to the specified issue
def showVideoCategorySpecificIssue(category_url, thumb, pub_title_index) :

	html 	= jw_common.loadUrl(category_url)
	soup 	= BeautifulSoup(html)

	pub_title_index = int(pub_title_index) #because it's a string actually !

	rows = soup.findAll('tr')

	pub_index_found = -1
	first_chapter_row = None
	last_chapter_row = None
	row_index = -1;

	for row in rows :
		row_index = row_index + 1
		row_class = None
		try:
			row_class = row["class"]
		except:
			pass

		if row_class is not None and row_class == 'pubTitle' :
			pub_index_found = pub_index_found + 1	
			continue

		if row_class is None and pub_index_found == pub_title_index:
			print "JWORG of searched pub issue"
			first_cell_class = row.findAll("td")[0]["class"]
			print first_cell_class
			if first_cell_class == "calign" :
				cell = row.findAll("td")[2]
			else :
				cell = row.findAll("td")[1]
			chapter_title = cell.contents[0].encode("utf-8")
			print chapter_title

			listItem = xbmcgui.ListItem(
				label 			= chapter_title, 
				thumbnailImage 	= thumb
			)

			params = { 
				"content_type" 		: "video", 
				"mode" 				: "open_sign_video_category_specific_row", 
				"url"				: category_url,
				"thumb" 			: thumb,
				"row_index"			: row_index
			} 

			url = jw_config.plugin_name + '?' + urllib.urlencode(params)
			xbmcplugin.addDirectoryItem(
				handle	 = jw_config.plugin_pid, 
				url 	 = url, 
				listitem = listItem, 
				isFolder = True 
			)  

	xbmcplugin.endOfDirectory(handle=jw_config.plugin_pid)	

