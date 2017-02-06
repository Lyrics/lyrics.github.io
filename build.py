#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
from urllib import quote
from xml.sax.saxutils import escape

siteURL = 'https://lyrics.github.io'
siteName = 'Lyrics'
srcDir = 'lyrics/database'
destDir = 'db'
indexFileName = 'index.html'
sitemapFileName = 'sitemap.xml'
searchFileName = 'search.html'
classNames = [ 'l', 'a', 'd', 'c' ] # letter, album, disc, composition

tLayout = open('templates/layout.hbs', 'r').read()
tHome = open('templates/home.hbs', 'r').read()
tSearch = open('templates/search.hbs', 'r').read()
t404 = open('templates/404.hbs', 'r').read()

def safePath(path):
    return path.lower().replace(' ', '-')

def encodeURL(path):
    return escape(quote(path, safe='/&\'"<>!()'))

def createHTML(path, filename):
    return open(os.path.join(path, filename), 'w')

def createXML():
    return open(sitemapFileName, 'w')

def createSearch():
    return open(searchFileName, 'w')

def printAnchor(target, content, depth):
    return '<li class="' + classNames[depth] + '"><a href="/' + encodeURL(target) + '/">' + content + '</a></li>'

def printSitemapURL(target, priority):
    URL = siteURL + '/' + encodeURL(target)
    if target:
        URL += '/'
    comeBack = 'daily'
    if priority < .8:
        comeBack = 'weekly'
    return '  <url>\n    <loc>' + URL + '</loc>\n  </url>\n'

def printBreadcrumbs(*items):
    output = ""
    depth = 0
    base = destDir
    for item in items:
        base = os.path.join(base, safePath(item))
        output += printAnchor(base, item, depth)
        depth += 1
    return output

def printDescriptionList(items):
    return ', '.join(items[:24])

def printDescriptionText(text):
    return re.sub(' +', ' ', text.replace('\n', ' ')[:220]).strip()

# 0. Create the root index file
main = createHTML('', indexFileName)
content = tLayout.replace('{{title}}', siteName)
content = content.replace('{{breadcrumbs}}', "")
content = content.replace('{{content}}', tHome)
content = content.replace('{{description}}', "Web interface to the lyrics database hosted on GitHub")
main.write(content)

# 0x. Define initial sitemap code
sitemapXML = '<?xml version="1.0" encoding="UTF-8"?>\n'
sitemapXML += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sitemapXML += printSitemapURL('', .31)

# 1. Loop through letters in the database
for letter in sorted(os.listdir(srcDir)):
    letterPath = os.path.join(srcDir, letter)
    if not os.path.isdir(letterPath):
        print letterPath + " is not a dir! 0x01"
    else:
        safeLetterPath = safePath(os.path.join(destDir, letter))
        # Create db/x/
        os.mkdir(safeLetterPath)
        # Create db/x/index.html
        letterPathFile = createHTML(safeLetterPath, indexFileName)
        letters = sorted(os.listdir(letterPath))
        letterList = ""
        sitemapXML += printSitemapURL(safeLetterPath, .56)

        # 2. Loop through artists starting with letter x
        for artist in letters:
            artistPath = os.path.join(letterPath, artist)
            if not os.path.isdir(artistPath):
                print artistPath + " is not a dir! 0x02"
            else:
                safeArtistPath = safePath(os.path.join(destDir, letter, artist))
                # Append artist link to db/x/index.html
                letterList += printAnchor(safeArtistPath, artist, 1)
                # Create db/x/artist/
                os.mkdir(safeArtistPath)
                # Create db/x/artist/index.html
                artistPathFile = createHTML(safeArtistPath, indexFileName)
                albums = sorted(os.listdir(artistPath))
                albumList = ""
                sitemapXML += printSitemapURL(safeArtistPath, .85)

                # 3. Loop through artist's albums
                for album in albums:
                    albumPath = os.path.join(artistPath, album)
                    if not os.path.isdir(albumPath):
                        print albumPath + " is not a dir! 0x03"
                    else:
                        safeAlbumPath = safePath(os.path.join(destDir, letter, artist, album))
                        # Append album link to db/x/artist/index.html
                        albumList += printAnchor(safeAlbumPath, album, 2)
                        # Create db/x/artist/album/
                        os.mkdir(safeAlbumPath)
                        # Create db/x/artist/album/index.htm
                        albumPathFile = createHTML(safeAlbumPath, indexFileName)
                        songs = sorted(os.listdir(albumPath))
                        songList = ""
                        sitemapXML += printSitemapURL(safeAlbumPath, .93)

                        # 4. Loop through songs
                        for song in songs:
                            songPath = os.path.join(albumPath, song)
                            if not os.path.isfile(songPath):
                                print songPath + " is not a file! 0x04"
                            else:
                                lyrics = open(songPath, 'r').read().strip()
                                safeSongPath = safePath(os.path.join(destDir, letter, artist, album, song))
                                # Append song link to db/x/artist/album/index.html
                                songList += printAnchor(safeSongPath, song, 3)
                                # Create db/x/artist/album/song/
                                os.mkdir(safeSongPath)
                                # Create db/x/artist/album/song/index.html
                                songPathFile = createHTML(safeSongPath, indexFileName)
                                # Populate it with lyrics
                                content = tLayout.replace('{{title}}', artist + ' – ' + song + ' | ' + siteName)
                                content = content.replace('{{breadcrumbs}}', printBreadcrumbs(letter, artist, album, song))
                                content = content.replace('{{content}}', '<pre>' + lyrics + '</pre>')
                                content = content.replace('{{description}}', printDescriptionText(lyrics))
                                songPathFile.write(content)
                                sitemapXML += printSitemapURL(safeSongPath, 1)

                        content = tLayout.replace('{{title}}', 'Album "' + album + '" by ' + artist + ' | ' + siteName)
                        content = content.replace('{{breadcrumbs}}', printBreadcrumbs(letter, artist, album))
                        content = content.replace('{{content}}', '<ul>' + songList + '</ul>')
                        content = content.replace('{{description}}', printDescriptionList(songs))
                        albumPathFile.write(content)

                content = tLayout.replace('{{title}}', artist + ' | ' + siteName)
                content = content.replace('{{breadcrumbs}}', printBreadcrumbs(letter, artist))
                content = content.replace('{{content}}', '<ul>' + albumList + '</ul>')
                content = content.replace('{{description}}', printDescriptionList(albums))
                artistPathFile.write(content)

        content = tLayout.replace('{{title}}', 'Artists starting with ' + letter + ' | ' + siteName)
        content = content.replace('{{breadcrumbs}}', printBreadcrumbs(letter))
        content = content.replace('{{content}}', '<ul>' + letterList + '</ul>')
        content = content.replace('{{description}}', printDescriptionList(letters))
        letterPathFile.write(content)

# 1x. Write the sitemap file
sitemapFile = createXML()
sitemapXML += '</urlset>\n'
sitemapFile.write(sitemapXML.encode('utf-8'))

# 1s. Generate the search page
search = createSearch()
content = tLayout.replace('{{title}}', 'Search' + ' | ' + siteName)
content = content.replace('{{breadcrumbs}}', '')
content = content.replace('{{content}}', tSearch)
content = content.replace('{{description}}', "Find lyrics using GitHub's code search engine")
search.write(content)

# 0e. Create the 404 page
four0four = createHTML('', '404.html')
content = tLayout.replace('{{title}}', siteName)
content = content.replace('{{breadcrumbs}}', '')
content = content.replace('{{content}}', t404)
content = content.replace('{{description}}', "Error #404: page not found. Apparently something got (re)moved.")
four0four.write(content)
