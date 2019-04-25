from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from urllib.parse import urlencode
import requests
import base64
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = '0ffe4f5e083f464f8ad6061cd80785ca'
redirect_uri1 = 'http://ec2-18-191-18-199.us-east-2.compute.amazonaws.com/callback/'
redirect_uri2 = 'http://ec2-18-191-18-199.us-east-2.compute.amazonaws.com/about'
token = 'NULL'


def test(request):
    return HttpResponse('<p1>Hi</p1>')


def home(request):
    HttpResponse('https://api.spotify.com/v1/artists/{3TVXtAsR1Inumwj472S9r4}')
    return render(request, 'authenticate/index.html')


def about(request):
    # info = playlist_list
    return render(request, 'authenticate/about.html')


def login(request):
    return redirect('https://accounts.spotify.com/authorize?client_id=' + client_id + '&response_type=code'
                    '&redirect_uri=' + redirect_uri1 + '&scope=user-read-private, user-read-recently-played, playlist-modify-public, playlist-modify-private')


def callback(request):
    code = request.GET.get('code', '')
    if code == '':
        print("AN ERROR OCCURRED, REDIRECTING HOME")
        return render(request, 'authenticate/index.html')
    url = 'https://accounts.spotify.com/api/token'
    encoded = base64.b64encode("{}:{}".format(client_id, os.environ['SPOTIPY_CLIENT_SECRET']).encode('utf-8')).decode(
        'utf-8')
    payload = {"grant_type": "authorization_code", "code": str(code), "redirect_uri": redirect_uri1}
    headers = {'Authorization': 'Basic ' + encoded}
    req = requests.post(url, data=payload, headers=headers)
    #print(req.text)
    global token
    response_list = req.json()
    token = response_list['access_token']
    print("TOKEN: " + token)

    client_credentials_manager = SpotifyClientCredentials(client_id=client_id,
                                                          client_secret=os.environ['SPOTIPY_CLIENT_SECRET'])
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # get users information
    headers = {'Authorization': 'Bearer ' + token}
    user = requests.get('https://api.spotify.com/v1/me', headers=headers)
    print("USER", user)
    resp = user.json()
    username = resp['id']
    playlists = sp.user_playlists(username)
    playlist_list = []
    name_id = {}
    while playlists:
        for playlist in playlists['items']:
            #playlist_list.append(playlist['name'])
            name_id[playlist['name']] = playlist['id']
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None

    context = {
        'playlist_list': name_id,
        'token': token,
    }
    request.session['playlist_list'] = name_id
    request.session['token'] = token
    # base_url = reverse('prune:choose')
    # query = urlencode({'context': context})
    # url = '{}?{}'.format(base_url, query)
    # return redirect(url)
    # return render(request, 'prune/choose.html/<token>', context)
    return render(request, 'prune/choose.html', context)



def refresh_token(request):
    return
