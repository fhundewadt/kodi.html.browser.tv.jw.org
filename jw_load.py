import urllib2
import json
import jw_config

def loadNotCachedUrl(url):
	response = urllib2.urlopen (url)
	html = response.read()
	return html		

def loadUrl (url):
	html = jw_config.cache.cacheFunction(loadNotCachedUrl, url)
	return html	

def loadNotCachedJsonFromUrl(url):
	response = urllib2.urlopen(url)
	data = json.load(response)

def loadJsonFromUrl (url):
	data = None
	try:
		# data = jw_config.cache.cacheFunction(loadNotCachedJsonFromUrl, url)	
		response = urllib2.urlopen(url)
		data = json.load(response)
	except:
		pass
	return data


