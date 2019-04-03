from django.shortcuts import render
from django.http import HttpResponse
import spotipy
import spotipy.util as util

def show_tracks(track_list):
    for i, item in enumerate(track_list['items']):
        track = item['track']
        print("   %d %32.32s %s" % (i, track['artists'][0]['name'], track['name']))

def home(request):
    HttpResponse('https://api.spotify.com/v1/artists/{3TVXtAsR1Inumwj472S9r4}')
    return render(request, 'authenticate/home.html')



def about(request):
    return render(request, 'authenticate/about.html')
