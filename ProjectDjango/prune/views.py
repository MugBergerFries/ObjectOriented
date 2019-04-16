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
    print("TEST123")
    #if request.method == 'POST':
    #print("LOOK HERE", request.POST.get())
    playlist_id = request.GET.get('playlist')
    #print("ID HERE", test)
    songs = requests.get('https://api.spotify.com/v1/playlists/'+test+'/tracks')
    resp = songs.json()
    print(resp)
    return render(request, 'prune/magic.html')
