from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
import requests
import os



def choose(request):
    # context = request.GET.get('context')
    # print("HERE IS CONTEXT",context)
    # playlist_chosen = request.POST.get('playlist')
    # print("LOOK HERE", playlist_chosen)
    return render(request, 'prune/choose.html')

def magic(request):
    playlist_id = request.GET.get('playlist')
    token = request.GET.get('token')
    headers = {'Authorization': 'Bearer ' + token}
    #print("ID HERE", test)
    recents = requests.get('https://api.spotify.com/v1/me/player/recently-played', headers=headers)
    # songs = requests.get('https://api.spotify.com/v1/playlists/'+playlist_id+'/tracks', headers=headers)
    # songs = songs.json()
    rec_resp = recents.json()
    for song in rec_resp:
        print(song)

    print(songs)
    print(song_names)
    return render(request, 'prune/magic.html')
