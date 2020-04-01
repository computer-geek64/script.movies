import sys
#import urllib
import xbmcgui
#import urlparse
import xbmcaddon


addon = xbmcaddon.Addon()
addon_name = addon.getAddonInfo('name')

# Get init data
base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
#args = urlparse.parse_qs(sys.argv[2][1:])
xbmcplugin.setContent(addon_handle, 'movies')
#mode = args.get('action', None)

# Functions
"""def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

# Set a string variable to use
line1 = 'This is a Kodi add-on'

# Launch a dialog box in kodi showing the string variable 'line1' as the contents
#xbmcgui.Dialog().ok(addonname, line1)


# Menu
if mode is None:
    listing = [
        (build_url({'action': 'listing', 'folder': 'movies'}), xbmcgui.ListItem('Movies', iconimage='DefaultFolder.png'), True),
        (build_url({'action': 'listing', 'folder': 'endpoints'}), xbmcgui.ListItem('Endpoints', iconImage='DefaultFolder.png'), True)
    ]
    xbmcplugin.addDirectoryItems(addon_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0] == 'pass':
    xbmcgui.Dialog().ok(addon_name, 'Welcome to ' + args['folder'][0] + '!')
"""
