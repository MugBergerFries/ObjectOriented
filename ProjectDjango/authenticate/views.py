from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
import urllib.parse
import requests
import base64
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = '0ffe4f5e083f464f8ad6061cd80785ca'
redirect_uri1 = 'http://ec2-18-191-18-199.us-east-2.compute.amazonaws.com/callback/'
redirect_uri2 = 'http://ec2-18-191-18-199.us-east-2.compute.amazonaws.com/about'
token = 'NULL'

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret='e1c15024a0c744a792d729510575a0ca')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlists = sp.user_playlists('1236360620')
while playlists:
    for playlist in playlists['items']:
        playlist_list.append(playlist['name'])
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None




def test(request):
    return HttpResponse(<p1>Hi</p1>)


def home(request):
    HttpResponse('https://api.spotify.com/v1/artists/{3TVXtAsR1Inumwj472S9r4}')
    return render(request, 'authenticate/index.html')


def about(request):
    info = playlist_list
    return render(request, 'authenticate/about.html')


def login(request):
    return redirect('https://accounts.spotify.com/authorize?client_id=' + client_id + '&response_type=code'
                    '&redirect_uri=' + redirect_uri1 + '&scope=user-read-private')


def callback(request):
    code = request.GET.get('code', '')
    if code == '':
        print("AN ERROR OCCURRED, REDIRECTING HOME")
        return render(request, 'authenticate/index.html')
    url = 'https://accounts.spotify.com/api/token'
    encoded = base64.b64encode("{}:{}".format(client_id, os.environ['SPOTIPY_CLIENT_SECRET']).encode('utf-8')).decode('utf-8')
    payload = {"grant_type": "authorization_code", "code": str(code), "redirect_uri": redirect_uri1}
    headers = {'Authorization': 'Basic ' + encoded}
    req = requests.post(url, data=payload, headers=headers)
    global token
    response_list = req.json()
    token = response_list['access_token']
    print("TOKEN: " + token)

    info = playlist_list
    return render(request, 'authenticate/about.html', info)


def refresh_token(request):
    return
