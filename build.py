#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
from urllib import quote
from xml.sax.saxutils import escape

siteURL = 'https://lyrics.github.io'
siteName = 'Lyrics'
srcDir = '../lyrics/database'
destDir = 'db'
indexFileName = 'index.html'
sitemapFileName = 'sitemap.xml'

tLayout = open('templates/layout.hbs', 'r').read()
tHome = open('templates/home.hbs', 'r').read()

def safePath(path):
    return path.lower().replace(' ', '-')

def encodeURL(path):
    #return path.replace('%', '%25').replace('?', '%3F')
    return escape(quote(path, safe='/&\'"<>'))

def createHTML(path):
    return open(os.path.join(path, indexFileName), 'w')

def createXML():
    return open(sitemapFileName, 'w')

def printAnchor(target, content):
    return '<li><a href="/' + encodeURL(target) + '/">' + content + '</a></li>'

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
    base = destDir
    for item in items:
        base = os.path.join(base, safePath(item))
        output += printAnchor(base, item)
    return output

def printDescriptionList(items):
    return ', '.join(items[:24])

def printDescriptionText(text):
    return re.sub(' +', ' ', text.replace('\n', ' ')[:140]).strip()

# 0. Create the root index file
main = createHTML('')
content = tLayout.replace('{{title}}', siteName)
content = content.replace('{{breadcrumbs}}', "")
content = content.replace('{{content}}', tHome)
content = content.replace('{{description}}', "Web interface to the lyrics database hosted on GitHub")
main.write(content)

# 0s. Define initial sitemap code
sitemapXML = '<?xml version="1.0" encoding="UTF-8"?>\n'
sitemapXML += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sitemapXML += printSitemapURL('', .31)
sitemapXML += printSitemapURL('db', .31)

# 1. Loop through letters in the database
for letter in sorted(os.listdir(srcDir)):
    letterPath = os.path.join(srcDir, letter)
    if not os.path.isdir(letterPath):
        print letterPath + " is not a dir! 0x01"
    else:
        safeLetterPath = safePath(os.path.join(destDir, letter))
        # Create db/X/
        os.mkdir(safeLetterPath)
        # Create db/X/index.html
        letterPathFile = createHTML(safeLetterPath)
        letters = sorted(os.listdir(letterPath))
        letterList = ""
        sitemapXML += printSitemapURL(safeLetterPath, .56)

        # 2. Loop through artists starting with letter X
        for artist in letters:
            artistPath = os.path.join(letterPath, artist)
            if not os.path.isdir(artistPath):
                print artistPath + " is not a dir! 0x02"
            else:
                safeArtistPath = safePath(os.path.join(destDir, letter, artist))
                # Append artist link to db/X/index.html
                letterList += printAnchor(safeArtistPath, artist)
                # Create db/X/artist/
                os.mkdir(safeArtistPath)
                # Create db/X/artist/index.html
                artistPathFile = createHTML(safeArtistPath)
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
                        # Append album link to db/X/artist/index.html
                        albumList += printAnchor(safeAlbumPath, album)
                        # Create db/X/artist/album/
                        os.mkdir(safeAlbumPath)
                        # Create db/X/artist/album/index.htm
                        albumPathFile = createHTML(safeAlbumPath)
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
                                # Append song link to db/X/artist/album/index.html
                                songList += printAnchor(safeSongPath, song)
                                # Create db/X/artist/album/song/
                                os.mkdir(safeSongPath)
                                # Create db/X/artist/album/song/index.html
                                songPathFile = createHTML(safeSongPath)
                                # Populate it with lyrics
                                content = tLayout.replace('{{title}}', artist + ' – ' + song + ' | ' + siteName)
                                content = content.replace('{{breadcrumbs}}', printBreadcrumbs(letter, artist, album, song))
                                content = content.replace('{{content}}', '<pre>' + escape(lyrics) + '</pre>')
                                content = content.replace('{{description}}', printDescriptionText(lyrics))
                                songPathFile.write(content)
                                sitemapXML += printSitemapURL(safeSongPath, 1)

                        content = tLayout.replace('{{title}}', 'Album ' + album + ' by ' + artist + ' | ' + siteName)
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

# 1s. Write the sitemap file
sitemapFile = createXML()
sitemapXML += '</urlset>\n'
sitemapFile.write(sitemapXML.encode('utf-8'))
