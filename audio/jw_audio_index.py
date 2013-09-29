import xbmcgui
import xbmcplugin

import urllib

import jw_config

# List of available audio services
def showAudioTypeIndex():
    
    # 1. Books of the bible
    listItem    = xbmcgui.ListItem( jw_config.t(30010) )    
    params      = {
        "content_type"  : "audio", 
        "mode"          : "open_bible_index"
    } 
    url = jw_config.plugin_name + '?' + urllib.urlencode(params)
    xbmcplugin.addDirectoryItem(
        handle      = jw_config.pluginPid, 
        url         = url, 
        listitem    = listItem, 
        isFolder    = True 
    )  
    
    # 2. Music and  songs
    listItem = xbmcgui.ListItem( jw_config.t(30011) )   
    params   = {
        "content_type"  : "audio", 
        "mode"          : "open_music_index", 
        "start"         : 0
    } 
    url = jw_config.plugin_name + '?' + urllib.urlencode(params)
    xbmcplugin.addDirectoryItem(
        handle      = jw_config.pluginPid, 
        url         = url, 
        listitem    = listItem, 
        isFolder    = True 
    )  

    # 2. Bible dramas
    listItem = xbmcgui.ListItem( jw_config.t(30013) )   
    params   = {
        "content_type"  : "audio", 
        "mode"          : "open_drama_index", 
        "start"         : 0
    } 
    url = jw_config.plugin_name + '?' + urllib.urlencode(params)
    xbmcplugin.addDirectoryItem(
        handle      = jw_config.pluginPid, 
        url         = url, 
        listitem    = listItem, 
        isFolder    = True 
    )  
    
    # 3. Dramatic bible reading
    listItem = xbmcgui.ListItem( jw_config.t(30014) )   
    params   = {
        "content_type"  : "audio", 
        "mode"          : "open_dramatic_reading_index", 
        "start"         : 0
    } 
    url = jw_config.plugin_name + '?' + urllib.urlencode(params)
    xbmcplugin.addDirectoryItem(
        handle      = jw_config.pluginPid, 
        url         = url, 
        listitem    = listItem, 
        isFolder    = True 
    )      
    
    xbmcplugin.endOfDirectory(handle=jw_config.pluginPid)