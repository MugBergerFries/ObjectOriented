from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
import requests
import os


class Song:
    def __init__(self, song_id, token):
        headers = {'Authorization': 'Bearer ' + token}
        song_info = requests.get('https://api.spotify.com/v1/audio-features/' + song_id, headers=headers)
        self.token = token
        self.key = song_info.json()['key']
        self.mode = song_info.json()['mode']
        self.acousticness = song_info.json()['acousticness']
        self.danceability = song_info.json()['danceability']
        self.energy = song_info.json()['energy']
        self.instrumentalness = round(song_info.json()['instrumentalness'])
        self.valence = song_info.json()['valence']
        self.tempo = song_info.json()['tempo']
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

    def closeness(self, song_2_id):  # returns a number 0-10, higher is closer
        song_2 = Song(song_2_id, self.token)
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
        headers = {'Authorization': 'Bearer ' + token}
        # recents = requests.get('https://api.spotify.com/v1/me/player/recently-played', headers=headers)
        songs = requests.get('https://api.spotify.com/v1/playlists/' + playlist_id + '/tracks', headers=headers)
        songs_resp = songs.json()
        tracks = songs_resp['items']
        id_list = []
        for p_track in tracks:
            id_list.append(p_track['track']['id'])
        song_list = []
        for song_id in id_list:
            song_list.append(Song(song_id, token))
        self.song_dict = dict(zip(id_list, song_list))
        average_names = ['key', 'mode', 'acousticness', 'danceability', 'energy', 'instrumentalness',
                         'valence', 'tempo']
        average_values = [0, 0, 0, 0, 0, 0, 0, 0]
        for song in self.song_dict.values():
            average_values = list(map(lambda x, y: x + y, average_values, song.attributes))
        average_values = list(map(lambda x: x / len(self.song_dict), average_values))
        self.averages = dict(zip(average_names, average_values))


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
    print(chosen.averages)
    context = {'to_prune': to_prune}
    return render(request, 'prune/magic.html', context)
