from django.shortcuts import render
from django.shortcuts import redirect
import requests


# This class represents a song and all the data related to it
class Song:
    def __init__(self, song_id, token, position):  # Constructor takes song id, user's token, and song # in playlist
        headers = {'Authorization': 'Bearer ' + token}  # Header for song info/attribute requests
        song_info = requests.get('https://api.spotify.com/v1/tracks/' + song_id, headers=headers)
        song_attributes = requests.get('https://api.spotify.com/v1/audio-features/' + song_id, headers=headers)
        # Song_info is basic information about song: name, id, etc. attributes describe what the song is like
        self.name = song_info.json()['name']  # Name of song
        self.position = position  # Position of song in playlist (0 is first)
        self.song_id = song_id  # ID of song in Spotify API
        self.token = token  # User's token
        self.key = song_attributes.json()['key']  # Key the song is in (0 is C, 1 is C#, 2 is D, etc.)
        self.mode = song_attributes.json()['mode']  # Major or minor (1 is major, 0 is minor)
        self.acousticness = song_attributes.json()['acousticness']  # Confidence of whether track is acoustic 0-1
        self.danceability = song_attributes.json()['danceability']  # How good for dancing the song is 0-1
        self.energy = song_attributes.json()['energy']  # Intensity and activity of song 0-1
        self.instrumentalness = round(song_attributes.json()['instrumentalness'])  # Whether the song has no words 0-1
        self.valence = song_attributes.json()['valence']  # Positivity of the track 0-1 (happy, cheerful, etc)
        self.tempo = song_attributes.json()['tempo']  # Estimated tempo of the song in BPM
        self.attributes = [self.key, self.mode, self.acousticness, self.danceability, self.energy,
                           self.instrumentalness, self.valence, self.tempo]  # List of the attributes of the song

    @staticmethod
    # Compares an attribute from 2 songs, returns a number 0-10, where 10 is the same and 0 is as far apart as possible
    def compare_attribute(value1, value2, attrmin, attrmax):
        maxdiff = attrmax - attrmin
        diff = abs(value1 - value2)
        if diff / maxdiff > 1:
            return 0
        else:
            return 10 * (1 - (diff / maxdiff))

    def closeness(self, invar):  # Returns a number 0-10, higher means the songs are more similar
        if type(invar) is dict:  # If passed variable is a dictionary
            kdiff = self.compare_attribute(self.key, invar['key'], 0, 11)
            mdiff = self.compare_attribute(self.mode, invar['mode'], 0, 1)
            adiff = self.compare_attribute(self.acousticness, invar['acousticness'], 0, 1)
            ddiff = self.compare_attribute(self.danceability, invar['danceability'], 0, 1)
            ediff = self.compare_attribute(self.energy, invar['energy'], 0, 1)
            idiff = self.compare_attribute(self.instrumentalness, invar['instrumentalness'], 0, 1)
            vdiff = self.compare_attribute(self.valence, invar['valence'], 0, 1)
            tdiff = self.compare_attribute(self.tempo, invar['tempo'], 55, 200)
            diffs = [kdiff, mdiff, adiff, ddiff, ediff, idiff, vdiff, tdiff]
        else:  # If passed variable is a Song object
            song_2 = Song(invar, self.token, -1)
            kdiff = self.compare_attribute(self.key, song_2.key, 0, 11)
            mdiff = self.compare_attribute(self.mode, song_2.mode, 0, 1)
            adiff = self.compare_attribute(self.acousticness, song_2.acousticness, 0, 1)
            ddiff = self.compare_attribute(self.danceability, song_2.danceability, 0, 1)
            ediff = self.compare_attribute(self.energy, song_2.energy, 0, 1)
            idiff = self.compare_attribute(self.instrumentalness, song_2.instrumentalness, 0, 1)
            vdiff = self.compare_attribute(self.valence, song_2.valence, 0, 1)
            tdiff = self.compare_attribute(self.tempo, song_2.tempo, 55, 200)
            diffs = [kdiff, mdiff, adiff, ddiff, ediff, idiff, vdiff, tdiff]
        return sum(diffs) / 8


# This class represents a playlist and contains all the songs in it in Song format
class Playlist:
    def __init__(self, playlist_id, token):
        self.token = token  # User's token
        headers = {'Authorization': 'Bearer ' + token}  # Header for API request to get all the songs
        songs = requests.get('https://api.spotify.com/v1/playlists/' + playlist_id + '/tracks', headers=headers)
        songs_resp = songs.json()  # Convert to json format
        tracks = songs_resp['items']  # Get list of tracks from response
        id_list = []
        for p_track in tracks:  # Convert Spotify's song to list to our format
            id_list.append(p_track['track']['id'])
        song_list = []
        for idx, song_id in enumerate(id_list):
            song_list.append(Song(song_id, token, idx))  # Make a Song object for each song
        self.song_dict = dict(zip(id_list, song_list))  # Turn list of IDs and Songs into a dict
        average_names = ['key', 'mode', 'acousticness', 'danceability', 'energy', 'instrumentalness',
                         'valence', 'tempo']
        average_values = [0, 0, 0, 0, 0, 0, 0, 0]
        for song in self.song_dict.values():  # Fond the average value for each attribute from all songs in playlist
            average_values = list(map(lambda x, y: x + y, average_values, song.attributes))
        average_values = list(map(lambda x: x / len(self.song_dict), average_values))
        self.averages = dict(zip(average_names, average_values))  # Dictionary of average attributes for this playlist

    # Finds the song in the playlist least like the average
    def find_song_to_prune(self):
        current_to_prune = 'undefined'
        lowest_closeness = 11
        for song in self.song_dict.values():
            if song.closeness(self.averages) < lowest_closeness:
                lowest_closeness = song.closeness(self.averages)
                current_to_prune = song.song_id
        return self.song_dict.get(current_to_prune, 'undefined')


# Next page, has the user choose their playlist to change at choose.html
def choose(request):
    playlist_dict = request.session.get('playlist_dict')  # Get the playlists from the session
    context = {  # This will be passed to choose.html
        'playlist_dict': playlist_dict
    }
    return render(request, 'prune/choose.html', context)


# The page where the chosen playlist is examined to find the song to be removed
def magic(request):
    if request.GET.get('playlist'):  # This if is to cleanse the url and hide variables passed in http. On first
        # visit, magic strips the variables from the http request and saves them to session. It sends them back
        # without the http variables, skipping the if
        playlist_id = request.GET.get('playlist')  # Retrieve chosen playlist ID (given to us from choose.html)
        request.session['playlist_id'] = playlist_id  # Save chosen playlist to session
        return redirect('/prune/magic')
    playlist_id = request.session.get('playlist_id')  # Retrieve chosen playlist from session
    token = request.session.get('token')  # Retrieve user's token from session
    chosen = Playlist(playlist_id, token)  # Make a Playlist object for the chosen playlist
    to_prune = chosen.find_song_to_prune()  # Find the song to remove
    if to_prune == 'undefined':
        print("ERROR: SONG CHOSEN TO PRUNE IS UNDEFINED")
        return render(request, 'prune/error.html')
    # Once song is chosen to prune, pass its id, name, position in the playlist, and it's playlist id to magic.html
    context = {'to_prune_id': to_prune.song_id, 'to_prune_name': to_prune.name, 'to_prune_pos': to_prune.position,
               'to_prune_token': to_prune.token, 'to_prune_playlist': playlist_id, 'compare_attr':
                   zip(chosen.averages.items(), to_prune.attributes)}
    return render(request, 'prune/magic.html', context)


# The page where the user is asked whether or not to remove the chosen song, and given a song preview
def remove(request):
    # Retrieve song id, position, token, and playlist id of song to be remove, save to the session, send the user back
    if request.GET.get('song_id'):  # Another if to cleanse the url from revealing variables.
        song_id = request.GET.get('song_id')
        request.session['song_id'] = song_id
        order = int(request.GET.get('order'))
        request.session['order'] = order
        token = request.GET.get('token')
        request.session['remove_token'] = token
        playlist_id = request.GET.get('playlist')
        request.session['remove_playlist_id'] = playlist_id
        return redirect('/prune/remove')
    # Get the song id, position, token, and playlist id from the session
    song_id = request.session.get('song_id')
    order = request.session.get('order')
    token = request.session.get('remove_token')
    playlist_id = request.session.get('remove_playlist_id')
    headers = {'Authorization': 'Bearer ' + token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
    # This the format the Spotify API expects for data on what song to delete
    data = '{"tracks":[{"uri":"spotify:track:' + song_id + '","positions":[' + str(order) + ']}]}'
    # Call Spotify api to delete song from a playlist
    requests.delete('https://api.spotify.com/v1/playlists/' + playlist_id + '/tracks', headers=headers, data=data)
    context = {'remove_song_id': song_id, 'remove_order': order, 'remove_token': token}
    return render(request, 'prune/remove.html', context)
