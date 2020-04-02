import os
import sys
import json
import urllib
import xbmcgui
import urlparse
import xbmcaddon
import xbmcplugin
from datetime import datetime


# Variables
tmdb_api_token = ''
laptop_ip = ''
kalistorm_ip = ''
kalistorm_port = 80
kalistorm_auth = {'username': '', 'password': ''}
kalistorm_api_token = ''


addon = xbmcaddon.Addon()
addon_name = addon.getAddonInfo('name')

# Get init data
base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
xbmcplugin.setContent(addon_handle, 'movies')
mode = args.get('action', None)

# Functions
def build_url(query):
    return base_url + '?' + urllib.urlencode(query)


# Menu
if mode is None:
    listing = [
        (build_url({'action': 'listing', 'folder': 'movies'}), xbmcgui.ListItem('Movies'), True),
        (build_url({'action': 'listing', 'folder': 'now_playing', 'page': 1}), xbmcgui.ListItem('Now Playing'), True),
        (build_url({'action': 'listing', 'folder': 'popular', 'page': 1}), xbmcgui.ListItem('Popular'), True),
        (build_url({'action': 'listing', 'folder': 'top_rated', 'page': 1}), xbmcgui.ListItem('Top Rated'), True),
        (build_url({'action': 'listing', 'folder': 'years'}), xbmcgui.ListItem('Years'), True)
    ]
    xbmcplugin.addDirectoryItems(addon_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0] == 'listing':
    #xbmcgui.Dialog().ok(addon_name, 'Welcome to ' + args['folder'][0] + '!')
    if args['folder'][0] == 'movies':
        response = urllib.urlopen('http://' + kalistorm_ip + '/kalistorm/api/movies?token=' + kalistorm_api_token)
        results = json.loads(response.read())
        listing = []
        for i in range(len(results['movies'])):
            list_item = xbmcgui.ListItem(results['movies'][i]['name'])
            list_item.setInfo('video', {'title': results['movies'][i]['name']})
            list_item.setProperty('IsPlayable', 'true')
            listing.append((build_url({'action': 'play_movie', 'movie': results['movies'][i]['name']}), list_item, False))
        xbmcplugin.addDirectoryItems(addon_handle, listing, len(listing))
        xbmcplugin.endOfDirectory(addon_handle)
    elif args['folder'][0] == 'now_playing':
        response = urllib.urlopen('https://api.themoviedb.org/3/movie/now_playing?api_key=' + tmdb_api_token + '&page=' + args['page'][0])
        results = json.loads(response.read())
        listing = []
        for i in range(len(results['results'])):
            title = results['results'][i]['title'].encode(errors='ignore')
            year = int(results['results'][i]['release_date'][:4].encode(errors='ignore'))
            rating = results['results'][i]['vote_average']
            plot = results['results'][i]['overview'].encode(errors='ignore')
            art = {}
            image_base_url = 'https://image.tmdb.org/t/p/w1280'
            if results['results'][i]['poster_path']:
                poster = results['results'][i]['poster_path'].encode(errors='ignore')[1:]
                art['poster'] = os.path.join(image_base_url, poster)
            if results['results'][i]['backdrop_path']:
                fanart = results['results'][i]['backdrop_path'].encode(errors='ignore')[1:]
                art['fanart'] = os.path.join(image_base_url, fanart)
            list_item = xbmcgui.ListItem(title)
            list_item.setInfo('video', {'title': title, 'year': year, 'rating': rating, 'plot': plot})
            list_item.setArt(art)
            list_item.setProperty('IsPlayable', 'true')
            listing.append((build_url({'action': 'play_movie', 'movie': title}), list_item, False))
        if int(args['page'][0]) < results['total_pages']:
            listing.append((build_url({'action': 'listing', 'folder': 'now_playing', 'page': int(args['page'][0]) + 1}), xbmcgui.ListItem('Next Page'), True))
        xbmcplugin.addDirectoryItems(addon_handle, listing, len(listing))
        xbmcplugin.endOfDirectory(addon_handle)
    elif args['folder'][0] == 'popular':
        response = urllib.urlopen('https://api.themoviedb.org/3/movie/popular?api_key=' + tmdb_api_token + '&page=' + args['page'][0])
        results = json.loads(response.read())
        listing = []
        for i in range(len(results['results'])):
            title = str(results['results'][i]['title'].encode(errors='ignore'))
            year = int(results['results'][i]['release_date'][:4].encode(errors='ignore'))
            rating = results['results'][i]['vote_average']
            plot = str(results['results'][i]['overview'].encode(errors='ignore'))
            art = {}
            image_base_url = 'https://image.tmdb.org/t/p/w1280'
            if results['results'][i]['poster_path']:
                poster = results['results'][i]['poster_path'].encode(errors='ignore')[1:]
                art['poster'] = os.path.join(image_base_url, poster)
            if results['results'][i]['backdrop_path']:
                fanart = results['results'][i]['backdrop_path'].encode(errors='ignore')[1:]
                art['fanart'] = os.path.join(image_base_url, fanart)
            list_item = xbmcgui.ListItem(title)
            list_item.setInfo('video', {'title': title, 'year': year, 'rating': rating, 'plot': plot})
            list_item.setArt(art)
            list_item.setProperty('IsPlayable', 'true')
            listing.append((build_url({'action': 'play_movie', 'movie': title}), list_item, False))
        if int(args['page'][0]) < results['total_pages']:
            listing.append((build_url({'action': 'listing', 'folder': 'popular', 'page': int(args['page'][0]) + 1}), xbmcgui.ListItem('Next Page'), True))
        xbmcplugin.addDirectoryItems(addon_handle, listing, len(listing))
        xbmcplugin.endOfDirectory(addon_handle)
    elif args['folder'][0] == 'top_rated':
        response = urllib.urlopen('https://api.themoviedb.org/3/movie/top_rated?api_key=' + tmdb_api_token + '&page=' + args['page'][0])
        results = json.loads(response.read())
        listing = []
        for i in range(len(results['results'])):
            title = str(results['results'][i]['title'].encode(errors='ignore'))
            year = int(results['results'][i]['release_date'][:4].encode(errors='ignore'))
            rating = results['results'][i]['vote_average']
            plot = str(results['results'][i]['overview'].encode(errors='ignore'))
            art = {}
            image_base_url = 'https://image.tmdb.org/t/p/w1280'
            if results['results'][i]['poster_path']:
                poster = results['results'][i]['poster_path'].encode(errors='ignore')[1:]
                art['poster'] = os.path.join(image_base_url, poster)
            if results['results'][i]['backdrop_path']:
                fanart = results['results'][i]['backdrop_path'].encode(errors='ignore')[1:]
                art['fanart'] = os.path.join(image_base_url, fanart)
            list_item = xbmcgui.ListItem(title)
            list_item.setInfo('video', {'title': title, 'year': year, 'rating': rating, 'plot': plot})
            list_item.setArt(art)
            list_item.setProperty('IsPlayable', 'true')
            listing.append((build_url({'action': 'play_movie', 'movie': title}), list_item, False))
        if int(args['page'][0]) < results['total_pages']:
            listing.append((build_url({'action': 'listing', 'folder': 'top_rated', 'page': int(args['page'][0]) + 1}), xbmcgui.ListItem('Next Page'), True))
        xbmcplugin.addDirectoryItems(addon_handle, listing, len(listing))
        xbmcplugin.endOfDirectory(addon_handle)
    elif args['folder'][0] == 'years':
        listing = [(build_url({'action': 'listing', 'folder': str(i), 'page': 1}), xbmcgui.ListItem(str(i)), True) for i in range(datetime.now().year, 1989, -1)]
        xbmcplugin.addDirectoryItems(addon_handle, listing, len(listing))
        xbmcplugin.endOfDirectory(addon_handle)
    elif args['folder'][0].isdigit():
        response = urllib.urlopen('https://api.themoviedb.org/3/discover/movie?api_key=' + tmdb_api_token + '&year=' + args['folder'][0] + '&page=' + args['page'][0])
        results = json.loads(response.read())
        listing = []
        for i in range(len(results['results'])):
            title = str(results['results'][i]['title'].encode(errors='ignore'))
            year = int(results['results'][i]['release_date'][:4].encode(errors='ignore'))
            rating = results['results'][i]['vote_average']
            plot = str(results['results'][i]['overview'].encode(errors='ignore'))
            art = {}
            image_base_url = 'https://image.tmdb.org/t/p/w1280'
            if results['results'][i]['poster_path']:
                poster = results['results'][i]['poster_path'].encode(errors='ignore')[1:]
                art['poster'] = os.path.join(image_base_url, poster)
            if results['results'][i]['backdrop_path']:
                fanart = results['results'][i]['backdrop_path'].encode(errors='ignore')[1:]
                art['fanart'] = os.path.join(image_base_url, fanart)
            list_item = xbmcgui.ListItem(title)
            list_item.setInfo('video', {'title': title, 'year': year, 'rating': rating, 'plot': plot})
            list_item.setArt(art)
            list_item.setProperty('IsPlayable', 'true')
            listing.append((build_url({'action': 'play_movie', 'movie': title}), list_item, False))
        if int(args['page'][0]) < results['total_pages']:
            listing.append((build_url({'action': 'listing', 'folder': args['folder'][0], 'page': int(args['page'][0]) + 1}), xbmcgui.ListItem('Next Page'), True))
        xbmcplugin.addDirectoryItems(addon_handle, listing, len(listing))
        xbmcplugin.endOfDirectory(addon_handle)
elif mode[0] == 'play_movie':
    response = urllib.urlopen('http://' + kalistorm_ip + '/kalistorm/api/movies?token=' + kalistorm_api_token + '&' + urllib.urlencode({'movie': args['movie'][0].replace('\'', '').replace('\"', '').replace('&', '').replace(':', '')}))
    results = json.loads(response.read())
    if results['path'] == '':
        xbmcgui.Dialog().ok(addon_name, 'This movie has not been added to the server.')
    else:
        play_item = xbmcgui.ListItem(path='http://' + kalistorm_auth['username'] + ':' + kalistorm_auth['password'] + '@' + kalistorm_ip + ':' + str(kalistorm_port) + os.path.join('/movies/', urllib.quote(results['path'])))
        xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)
