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
	data = None
	try:
		response = urllib2.urlopen(url)
		data = json.load(response)
	except:
		pass
	return data

def loadJsonFromUrl (url):
	data = jw_config.cache.cacheFunction(loadNotCachedJsonFromUrl, url)	
	return data


