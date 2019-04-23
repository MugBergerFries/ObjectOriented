from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
import requests
import os


class Song:
    def __init__(self, song_id, token, position):
        headers = {'Authorization': 'Bearer ' + token}
        song_info = requests.get('https://api.spotify.com/v1/tracks/' + song_id, headers=headers)
        song_attributes = requests.get('https://api.spotify.com/v1/audio-features/' + song_id, headers=headers)
        print("THIS SONG: " + song_attributes.text)
        self.name = song_info.json()['name']
        self.position = position
        self.song_id = song_id
        self.token = token
        self.key = song_attributes.json()['key']
        self.mode = song_attributes.json()['mode']
        self.acousticness = song_attributes.json()['acousticness']
        self.danceability = song_attributes.json()['danceability']
        self.energy = song_attributes.json()['energy']
        self.instrumentalness = round(song_attributes.json()['instrumentalness'])
        self.valence = song_attributes.json()['valence']
        self.tempo = song_attributes.json()['tempo']
        self.attributes = [self.key, self.mode, self.acousticness, self.danceability, self.energy,
                           self.instrumentalness, self.valence, self.tempo]

    @staticmethod
    def compare_attribute(value1, value2, attrmin, attrmax):  # returns a number from 0-10, higher is closer
        maxdiff = attrmax - attrmin
        diff = abs(value1 - value2)
        if diff / maxdiff > 1:
            return 0
        else:
            return 10 * (1 - (diff / maxdiff))

    def closeness(self, invar):  # returns a number 0-10, higher is closer
        if type(invar) is dict:
            kdiff = self.compare_attribute(self.key, invar['key'], 0, 11)
            mdiff = self.compare_attribute(self.mode, invar['mode'], 0, 1)
            adiff = self.compare_attribute(self.acousticness, invar['acousticness'], 0, 1)
            ddiff = self.compare_attribute(self.danceability, invar['danceability'], 0, 1)
            ediff = self.compare_attribute(self.energy, invar['energy'], 0, 1)
            idiff = self.compare_attribute(self.instrumentalness, invar['instrumentalness'], 0, 1)
            vdiff = self.compare_attribute(self.valence, invar['valence'], 0, 1)
            tdiff = self.compare_attribute(self.tempo, invar['tempo'], 55, 200)
            diffs = [kdiff, mdiff, adiff, ddiff, ediff, idiff, vdiff, tdiff]
        else:
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


class Playlist:

    def __init__(self, playlist_id, token):
        self.token = token
        headers = {'Authorization': 'Bearer ' + token}
        # recents = requests.get('https://api.spotify.com/v1/me/player/recently-played', headers=headers)
        songs = requests.get('https://api.spotify.com/v1/playlists/' + playlist_id + '/tracks', headers=headers)
        songs_resp = songs.json()
        print('SONGS_RESP: ' + songs.text)
        tracks = songs_resp['items']
        id_list = []
        for p_track in tracks:
            id_list.append(p_track['track']['id'])
        song_list = []
        for idx, song_id in enumerate(id_list):
            song_list.append(Song(song_id, token, idx))
        self.song_dict = dict(zip(id_list, song_list))
        average_names = ['key', 'mode', 'acousticness', 'danceability', 'energy', 'instrumentalness',
                         'valence', 'tempo']
        average_values = [0, 0, 0, 0, 0, 0, 0, 0]
        for song in self.song_dict.values():
            average_values = list(map(lambda x, y: x + y, average_values, song.attributes))
        average_values = list(map(lambda x: x / len(self.song_dict), average_values))
        self.averages = dict(zip(average_names, average_values))

    def find_song_to_prune(self):
        current_to_prune = 'undefined'
        lowest_closeness = 11
        for song in self.song_dict.values():
            if song.closeness(self.averages) < lowest_closeness:
                lowest_closeness = song.closeness(self.averages)
                current_to_prune = song.song_id
        return self.song_dict.get(current_to_prune, 'undefined')


def choose(request):
    # context = request.GET.get('context')
    # print("HERE IS CONTEXT",context)
    # playlist_chosen = request.POST.get('playlist')
    # print("LOOK HERE", playlist_chosen)
    return render(request, 'prune/choose.html')


def magic(request):
    playlist_id = request.GET.get('playlist')
    token = request.GET.get('token')
    chosen = Playlist(playlist_id, token)
    to_prune = chosen.find_song_to_prune()
    if to_prune == 'undefined':
        print("ERROR: SONG CHOSEN TO PRUNE IS UNDEFINED")
        return render(request, 'prune/error.html')
    context = {'to_prune_id': to_prune.song_id, 'to_prune_name': to_prune.name, 'to_prune_pos': to_prune.position, 'to_prune_token': to_prune.token, 'to_prune_playlist':playlist_id}
    return render(request, 'prune/magic.html', context)

def remove(request):
    song_id = request.GET.get('song_id')
    order = request.GET.get('order')
    token = request.GET.get('token')
    playlist_id = request.GET.get('playlist')

    headers = {'Authorization': 'Bearer ' + token}
    tracks = {"tracks":[{"uri": "spotify:track:"+song_id, "positions":[order]}]}
    tracks = str(tracks)
    songs = requests.delete('https://api.spotify.com/v1/playlists/'+str(playlist_id)+'/tracks',  headers=headers, data=tracks)
    print("RESPONSE", songs)

    context = {'remove_song_id':song_id, 'remove_order':order, 'remove_token': token}
    return render(request, 'prune/remove.html', context)
