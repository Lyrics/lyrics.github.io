#!/usr/bin/env python

import os

siteName = 'Lyrics'
srcDir = '../lyrics/database'
destDir = 'db'
indexFileName = 'index.html'

tLayout = open('templates/layout.hbs', 'r').read()
tHome = open('templates/home.hbs', 'r').read()

def safePath(path):
    return path#.replace('/', '%2F')

def encodeURL(path):
    return path.replace('?', '%3F')

def createIndex(path):
    indexFile = open(os.path.join(path, indexFileName), 'w')
    return indexFile

def printAnchor(target, content):
    return '<li><a href="/' + encodeURL(target) + '/">' + content + '</a></li>'

def printBreadcrumbs(*items):
    output = ""
    base = destDir
    for item in items:
        base = os.path.join(base, safePath(item))
        output += printAnchor(base, item)
    return output

# 0. Create the root index file
main = createIndex('')
main.write(tLayout.replace('{{title}}', siteName).replace('{{breadcrumbs}}', "").replace('{{content}}', tHome))

# 1. Loop through letters in the database
for letter in sorted(os.listdir(srcDir)):
    letterPath = os.path.join(srcDir, letter)
    if not os.path.isdir(letterPath):
        print letterPath + " is not a dir! 0x01"
    else:
        safeLetterPath = os.path.join(destDir, letter)
        # Create db/X/
        os.mkdir(safeLetterPath)
        # Create db/X/index.html
        letterPathFile = createIndex(safeLetterPath)
        letterList = ""

        # 2. Loop through artists starting with letter X
        for artist in sorted(os.listdir(letterPath)):
            artistPath = os.path.join(letterPath, artist)
            if not os.path.isdir(artistPath):
                print artistPath + " is not a dir! 0x02"
            else:
                safeArtistPath = os.path.join(destDir, letter, safePath(artist))
                # Append artist link to db/X/index.html
                letterList += printAnchor(safeArtistPath, artist)
                # Create db/X/artist/
                os.mkdir(safeArtistPath)
                # Create db/X/artist/index.html
                artistPathFile = createIndex(safeArtistPath)
                albumList = ""

                # 3. Loop through artist's albums
                for album in sorted(os.listdir(artistPath)):
                    albumPath = os.path.join(artistPath, album)
                    if not os.path.isdir(albumPath):
                        print albumPath + " is not a dir! 0x03"
                    else:
                        safeAlbumPath = os.path.join(destDir, letter, safePath(artist), safePath(album))
                        # Append album link to db/X/artist/index.html
                        albumList += printAnchor(safeAlbumPath, album)
                        # Create db/X/artist/album/
                        os.mkdir(safeAlbumPath)
                        # Create db/X/artist/album/index.htm
                        albumPathFile = createIndex(safeAlbumPath)
                        songList = ""

                        # 4. Loop through songs
                        for song in sorted(os.listdir(albumPath)):
                            songPath = os.path.join(albumPath, song)
                            if not os.path.isfile(songPath):
                                print songPath + " is not a file! 0x04"
                            else:
                                lyrics = open(songPath, 'r').read().strip()
                                safeSongPath = os.path.join(destDir, letter, safePath(artist), safePath(album), safePath(song))
                                # Append song link to db/X/artist/album/index.html
                                songList += printAnchor(safeSongPath, song)
                                # Create db/X/artist/album/song/
                                os.mkdir(safeSongPath)
                                # Create db/X/artist/album/song/index.html
                                songPathFile = createIndex(safeSongPath)
                                # Populate it with lyrics
                                content = tLayout.replace('{{title}}', artist + ' - ' + song + ' | ' + siteName)
                                content = content.replace('{{breadcrumbs}}', printBreadcrumbs(letter, artist, album, song))
                                content = content.replace('{{content}}', '<pre>' + lyrics + '</pre>')
                                songPathFile.write(content)

                        content = tLayout.replace('{{title}}', album + ' by ' + artist + ' | ' + siteName)
                        content = content.replace('{{breadcrumbs}}', printBreadcrumbs(letter, artist, album))
                        content = content.replace('{{content}}', '<ul>' + songList + '</ul>')
                        albumPathFile.write(content)

                content = tLayout.replace('{{title}}', artist + ' | ' + siteName)
                content = content.replace('{{breadcrumbs}}', printBreadcrumbs(letter, artist))
                content = content.replace('{{content}}', '<ul>' + albumList + '</ul>')
                artistPathFile.write(content)

        content = tLayout.replace('{{title}}', 'Artists starting on ' + letter + ' | ' + siteName)
        content = content.replace('{{breadcrumbs}}', printBreadcrumbs(letter))
        content = content.replace('{{content}}', '<ul>' + letterList + '</ul>')
        letterPathFile.write(content)
