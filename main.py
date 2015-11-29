import pyen
import pprint
import sys
import spotipy
import spotipy.util as util
import os
from playlistTheme import *
from PyQt5.QtWidgets import (QWidget, QPushButton, 
    QLabel, QComboBox, QHBoxLayout, QSlider, QLabel,
    QLineEdit, QVBoxLayout, QApplication)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from Genres import *

###If not working, change the username!
###We need to ask for username!

# Set variables specific to our application.
os.environ['SPOTIPY_CLIENT_ID'] = '6abdfbaa139448b2b20bdbc8c85e6316'
os.environ['SPOTIPY_CLIENT_SECRET'] = 'dcc60e1288414f9e98dde464eea03d9b'
os.environ['SPOTIPY_REDIRECT_URI'] = 'http://google.ca'

# Initialize Echonest object.
en = pyen.Pyen('0QZ2JW9IHKZQ9BMKI')


# Set scope of application, see Spotify docs for info on scopes.
scope = 'playlist-modify-public playlist-modify-private user-library-modify user-library-read'

#Define out example class, inherits much of itself from QWidget module
class Example(QWidget):
    #Inherits parent class
    def __init__(self):
        super().__init__()
        #Initializes the UI upon instantiation
        self.initUI()
    #Method to make the UI much of it created from QTStudio and converted into usable python
    def initUI(self):
        #The genre drop down box
        genreCombo = QComboBox(self)
        #Some of the most popular genres
        genreCombo.addItem("Select Genre")
        genreCombo.addItem("Rap")
        genreCombo.addItem('Electronic')
        genreCombo.addItem("Techno")
        genreCombo.addItem("Rock")
        #Adds every genre on spotify to the list
        for i in range(len(genre_list)):
            genreCombo.addItem(genre_list[i])
        genreCombo.activated[str].connect(self.genreComboActivated)

        #The theme drop down box
        themeCombo = QComboBox(self)
        #Uses several base themes for tempo, loudness, etc...
        themeCombo.addItem("Select Theme")
        themeCombo.addItem("Workout")
        themeCombo.addItem('Study')
        themeCombo.addItem('Chill')
        themeCombo.addItem("Party")
        themeCombo.activated[str].connect(self.themeComboActivated)

        #A slider that creates an integer for use with the number of songs needed
        songCountSlider = QSlider(Qt.Horizontal, self)
        songCountSlider.setFocusPolicy(Qt.NoFocus)
        songCountSlider.setMinimum(1)
        songCountSlider.setMaximum(100)
        songCountSlider.valueChanged[int].connect(self.changeValue)

        #Labeled song count
        songCountLabel = QLabel('Song Count', self)

        #When pushed it runs the generatePlaylist method
        generatePlaylistPush = QPushButton('Generate Playlist', self)
        generatePlaylistPush.setToolTip('Generate your playlist!')
        generatePlaylistPush.clicked.connect(self.generatePlaylist)

        playlistNameForm = QLineEdit(self)
        playlistNameForm.setText('Enter Playlist Name')
        playlistNameForm.textChanged.connect(self.updatePlaylistName)

        # Layout control.
        hbox = QHBoxLayout()
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(vbox)
        vbox.addWidget(playlistNameForm)
        vbox.addWidget(songCountLabel)
        vbox.addWidget(songCountSlider)
        vbox.addWidget(genreCombo)
        vbox.addWidget(themeCombo)
        vbox.addWidget(generatePlaylistPush)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('Spotify Playlist Generator')  
        self.setWindowIcon(QIcon('spotify_256.png'))
        self.show()

    #A basic method for making the genre a global variable and clarifying that the script is working correctly
    def genreComboActivated(self, genre):
        global seedGenre
        seedGenre = genre.lower()
        if genre in ['Select Genre']:
            print('Please select a genre.')
        else:
            print('worked ' + genre)
        return seedGenre

    #A basic method for making the theme a global variable and clarifying that the script is working correctly
    def themeComboActivated(self, theme):
        global seedTheme
        seedTheme = theme.lower()
        if theme in ['Select Theme']:
            print('Please select a theme.')
        else:
            print('worked ' + theme)
        return seedTheme

    #A basic method for making the song count a global variable and clarifying that the script is working correctly
    def changeValue(self, value):
        global songCount
        songCount = value
        print(songCount)
        return songCount

    #A basic method for making the playlist name a global variable and clarifying that the script is working correctly
    def updatePlaylistName(self, text):
        global playlistName
        playlistName = text
        print(playlistName)

    #Generates the playlist
    def generatePlaylist(self):
        #Defines the user
        username = 'azzy6106'
        #Defines token from spotipy util
        token = util.prompt_for_user_token(username, scope)
        #Checks if token is true and defines sp if so as the user with token as its authentication
        if token:
            sp = spotipy.Spotify(auth = token)
        #Otherwise something went wrong
        else:
            print("Can't get token for", username)

        #Creates a playlist for the user
        sp.user_playlist_create(username, playlistName, public = True)
        newPlaylist = sp.user_playlists(username, limit = 1, offset = 0)
        #Gets the id of the playlist
        playListId = newPlaylist['items'][0]['uri']

        #From Echo Nest this checks the genre and gets results back
        response = en.get('playlist/dynamic/create', genre = seedGenre, type = 'genre-radio',bucket = ['id:spotify', 'tracks'])
        session_id = response['session_id']

        #In song count iterate through each element
        for song_count in range(songCount):
            #Assume the song does not exist until the server tells us it does
            songExists = False
            while not songExists:
                #Try to get the song and add it to a playlist
                try:
                    #From Echo Nest this gets a reponse of the next closest song match up
                    response = en.get('playlist/dynamic/next', session_id = session_id)
                    #Enumerates through the response of just the songs.
                    for i, s in enumerate(response['songs']):
                        #Prints the number of the song being added, the title, and the artists name
                        print("%d %s by %s" % (song_count + 1, s['title'], s['artist_name']))
                        #Adds the track to our playlist
                        sp.user_playlist_add_tracks(username, playListId, tracks = [s['tracks'][0]['foreign_id']], position = 0)
                        #If all of thiss has happened without error then the song must exist
                        songExists = True

                #The only error from this will be an index error because the song will not be in the index so if that happens try this instead
                except IndexError:
                    #This tells the user that it does not have a proper id and because we assume the song does not exist it will skip this song and try again
                    print('song does not have proper id')
                finally:
                    print(end = '')
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())