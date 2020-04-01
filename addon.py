import sys
import xbmcgui
import xbmcaddon


addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')

# Set plugin type to movies
addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'movies')

# Set a string variable to use
line1 = 'This is a Kodi add-on'

# Launch a dialog box in kodi showing the string variable 'line1' as the contents
xbmcgui.Dialog().ok(addonname, line1)
