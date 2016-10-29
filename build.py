#!/usr/bin/env python

import os

siteName = 'Lyrics'
srcDir = 'lyrics/database'
destDir = 'db'

HTMLheader = open( 'partials/header_start.htm', 'r' ).read().strip()
HTMLhedend = open( 'partials/header_end.htm', 'r' ).read().strip()
HTMLfooter = open( 'partials/footer.htm', 'r' ).read()

def simplifyPath( s ):
    return s.replace( ' ', '-' ).lower()

def createIndex( path, title ):
    indexFile = open( os.path.join( path, 'index.htm' ), 'w' )
    indexFile.write( HTMLheader + title + HTMLhedend )
    return indexFile

def anchor( target, content ):
    return '<a href="/' + target + '">' + content + '</a>'

main = createIndex( '', siteName )
main.write( "Welcome!" )
main.write( HTMLfooter )

for letter in os.listdir( srcDir ):
    letterPath = os.path.join( srcDir, letter )
    if not os.path.isdir( letterPath ):
        print letterPath + " is not a dir!"
    else:
        simplifiedLetterPath = simplifyPath( os.path.join(destDir, letter) )
        # Create db/x/
        os.mkdir( simplifiedLetterPath )
        # Create db/x/index.htm
        letterPathFile = createIndex( simplifiedLetterPath, " | " + siteName )
        for artist in os.listdir( letterPath ):
            artistPath = os.path.join( letterPath, artist )
            if not os.path.isdir( artistPath ):
                print artistPath + " is not a dir!"
            else:
                simplifiedArtistPath = simplifyPath( os.path.join( destDir, letter, artist ) )
                # Append artist link to db/x/index.htm
                letterPathFile.write( anchor( simplifiedArtistPath, artist ) )
                # Create db/x/artist/
                os.mkdir( simplifiedArtistPath )
                # Create db/x/artist/index.htm
                artistPathFile = createIndex( simplifiedArtistPath, " | " + siteName )
                for album in os.listdir( artistPath ):
                    albumPath = os.path.join( artistPath, album )
                    if not os.path.isdir( albumPath ):
                        print albumPath + " is not a dir!"
                    else:
                        simplifiedAlbumPath = simplifyPath( os.path.join( destDir, letter, artist, album ) )
                        # Append album link to db/x/artist/index.htm
                        artistPathFile.write( anchor( simplifiedAlbumPath, album ) )
                        # Create db/x/artist/album/
                        os.mkdir( simplifiedAlbumPath )
                        # Create db/x/artist/album/index.htm
                        albumPathFile = createIndex( simplifiedAlbumPath, " | " + siteName )
                        for song in os.listdir( albumPath ):
                            songPath = os.path.join( albumPath, song )
                            if not os.path.isfile( songPath ):
                                print songPath + " is not a file!"
                            else:
                                lyrics = open( songPath, 'r' ).read()
                                simplifiedSongPath = simplifyPath( os.path.join( destDir, letter, artist, album, song ) )
                                # Append song link to db/x/artist/album/index.htm
                                albumPathFile.write( anchor( simplifiedSongPath, song ) )
                                # Create db/x/artist/album/song/
                                os.mkdir( simplifiedSongPath )
                                # Create db/x/artist/album/song/index.htm
                                songPathFile = createIndex( simplifiedSongPath, " | " + siteName )
                                # Also create a plaintext file
                                txt = open( simplifiedSongPath + '.txt', 'w' )
                                # Populate them with lyrics
                                txt.write( lyrics )
                                songPathFile.write( '<pre>' + lyrics + '</pre>' )
                                songPathFile.write( HTMLfooter )
                        albumPathFile.write( HTMLfooter )
                artistPathFile.write( HTMLfooter )
        letterPathFile.write( HTMLfooter )
