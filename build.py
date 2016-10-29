#!/usr/bin/env python

import os

srcDir = 'lyrics/database'
destDir = 'db'

HTMLheader = '<!doctype html><meta charset="utf-8"/><title>'
HTMLhedend = '</title><div>'
HTMLfooter = '</div>'

def simplifyPath( string ):
    return string.replace( ' ', '-' ).lower()

def createIndex( path ):
    f = open( os.path.join( path, 'index.htm' ), 'w+' )
    f.write( HTMLheader + HTMLhedend )
    return f

for letter in os.listdir( srcDir ):
    letterPath = os.path.join( srcDir, letter )
    if not os.path.isdir( letterPath ):
        print letterPath + " is not a dir!"
    else:
        simplifiedLetterPath = simplifyPath( os.path.join(destDir, letter) )
        # Create db/x/
        os.mkdir( simplifiedLetterPath )
        # Create db/x/index.htm
        letterPathFile = createIndex( simplifiedLetterPath )
        for artist in os.listdir( letterPath ):
            artistPath = os.path.join( letterPath, artist )
            if not os.path.isdir( artistPath ):
                print artistPath + " is not a dir!"
            else:
                simplifiedArtistPath = simplifyPath( os.path.join( destDir, letter, artist ) )
                # Append artist link to db/x/index.htm
                letterPathFile.write( artist )
                # Create db/x/artist/
                os.mkdir( simplifiedArtistPath )
                # Create db/x/artist/index.htm
                artistPathFile = createIndex( simplifiedArtistPath )
                for album in os.listdir( artistPath ):
                    albumPath = os.path.join( artistPath, album )
                    if not os.path.isdir( albumPath ):
                        print albumPath + " is not a dir!"
                    else:
                        simplifiedAlbumPath = simplifyPath( os.path.join( destDir, letter, artist, album ) )
                        # Append album link to db/x/artist/index.htm
                        artistPathFile.write( album )
                        # Create db/x/artist/album/
                        os.mkdir( simplifiedAlbumPath )
                        # create db/x/artist/album/index.htm
                        albumPathFile = createIndex( simplifiedAlbumPath )
                        for song in os.listdir( albumPath ):
                            songPath = os.path.join( albumPath, song )
                            if not os.path.isfile( songPath ):
                                print songPath + " is not a file!"
                            else:
                                simplifiedSongPath = simplifyPath( os.path.join( destDir, letter, artist, album, song ) )
                                # Append song link to db/x/artist/album/index.htm
                                albumPathFile.write( song )
                                # Create db/x/artist/album/song/
                                os.mkdir( simplifiedSongPath )
                                # Create db/x/artist/album/song/index.htm
                                songPathFile = createIndex( simplifiedSongPath )
                                # populate it with the song's contents
        letterPathFile.write( HTMLfooter )
