from django.shortcuts import render
from django.shortcuts import redirect
import requests
import base64
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = '0ffe4f5e083f464f8ad6061cd80785ca'  # Spotify ID of our application client
redirect_uri1 = 'http://tidytunes.org/callback/'  # Redirect URIs used by Spotify
redirect_uri2 = 'http://tidytunes.org/about'  # They tell Spotify where to send the user after authentication
token = 'NULL'  # User's token to show Spotify we have access to their data


# First function to be run, simply returns our home page, index.html
def home(request):
    return render(request, 'authenticate/index.html')


# Return our page displaying users playlists
def about(request):
    return render(request, 'authenticate/about.html')


# Logging user in, asking for permission for our scope
def login(request):
    return redirect('https://accounts.spotify.com/authorize?client_id=' + client_id + '&response_type=code'
                    '&redirect_uri=' + redirect_uri1 + '&scope=user-read-private, user-read-recently-played,'
                                                       'playlist-modify-public, playlist-modify-private')


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
    global token
    response_list = req.json()
    token = response_list['access_token']
    print("TOKEN: " + token)
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id,
                                                          client_secret=os.environ['SPOTIPY_CLIENT_SECRET'])
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    # get users information using Spotipy and Spotify API
    headers = {'Authorization': 'Bearer ' + token}
    # getting username from Spotify api then converting to json format
    user = requests.get('https://api.spotify.com/v1/me', headers=headers)
    resp = user.json()
    username = resp['id']
    # use the username to get their playlists, then create a dict that has playlist name as key, playlist key as value
    playlists = sp.user_playlists(username)
    name_id = {}
    while playlists:
        for playlist in playlists['items']:
            name_id[playlist['name']] = playlist['id']
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None
    # What we pass to the choose.html page. It will have access to our playlist/id dict and the token the user obtained
    context = {
        'playlist_list': name_id
    }
    request.session['token'] = token
    return render(request, 'prune/choose.html', context)


def refresh_token(request):
    return
