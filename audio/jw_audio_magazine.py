import jw_common
import jw_config

import urllib
import sys

import xbmcgui
import xbmcplugin

def showMagazineIndex(pub_filter = None, year_filter = None):

    print sys.argv
    print "JWORG showMagazineIndex"

    if pub_filter is None:

        print "pub_filter is None"

        items = [
            {   "title" : jw_common.t(30026),  
                "mode"  : "open_magazine_index",    
                "pub_filter" : " " ,
                "year_filter" : "" 
            },
            {   "title" : jw_common.t(30027),  
                "mode"  : "open_magazine_index",    
                "pub_filter" : "g"  ,
                "year_filter" : "" 
            },
            {   "title" : jw_common.t(30028),  
                "mode"  : "open_magazine_index",    
                "pub_filter" : "wp" ,
                "year_filter" : "" 
            },
            {   "title" : jw_common.t(30029),  
                "mode"  : "open_magazine_index", 	
                "pub_filter" : "w"  ,
                "year_filter" : "" 
            },
            {   "title" : jw_common.t(30030),  
                "mode"  : "open_magazine_index",    
                "pub_filter" : "ws" ,
                "year_filter" : "" 
            },
        ]

    if pub_filter is not None and year_filter is None:

        print "pub_filter is " + pub_filter + ", year filter is None"

        items = []

        for year in [" ", "2010", "2011", "2012", "2013"]: 
            title = year
            if title == " " :
                title = jw_common.t(30031)

            items.append ({  
                "title"         : title,  
                "mode"          : "open_magazine_index",    
                "pub_filter"    : pub_filter,
                "year_filter"   : year
            })

    if pub_filter is not None and year_filter is not None:

        print "pub_filter is " + pub_filter + ", year filter is " + year_filter

        language        = jw_config.language
        magazine_url    = jw_config.const[language]["magazine_index"] + "?pubFilter=" + pub_filter + "&yearFilter=" + year_filter
        html            = jw_common.loadUrl(magazine_url) 

        print "JWORG magazine url: " + magazine_url
        print html

        items = []

    print "JWORG Adding items"
    print items

    for item in items:

        if item["title"] == "-" :
            continue

        listItem    = xbmcgui.ListItem( item["title"] )     

        params      = {
            "content_type"  : "audio", 
            "mode"          : item["mode"],
            "pub_filter"	: item["pub_filter"],
            "year_filter"   : item["year_filter"]
        } 

        url = jw_config.plugin_name + '?' + urllib.urlencode(params)
        print url
        xbmcplugin.addDirectoryItem(
            handle      = jw_config.pluginPid, 
            url         = url, 
            listitem    = listItem, 
            isFolder    = True 
        )  
    
    xbmcplugin.endOfDirectory(handle=jw_config.pluginPid)