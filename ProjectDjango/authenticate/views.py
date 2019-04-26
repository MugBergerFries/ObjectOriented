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


# This part strips the code given by Spotify and obtains the user's token. It also gets the users playlists
def callback(request):
    code = request.GET.get('code', '')  # Get the code sent by Spotify
    if code == '':
        print("AN ERROR OCCURRED, REDIRECTING HOME")
        return render(request, 'authenticate/index.html')
    url = 'https://accounts.spotify.com/api/token'  # URL to obtain token
    encoded = base64.b64encode("{}:{}".format(client_id, os.environ['SPOTIPY_CLIENT_SECRET']).encode('utf-8')).decode(
        'utf-8')  # Used in token header, should be "client_id:secret" encoded in base64
    payload = {"grant_type": "authorization_code", "code": str(code), "redirect_uri": redirect_uri1}  # Body of request
    headers = {'Authorization': 'Basic ' + encoded}  # Header of request
    req = requests.post(url, data=payload, headers=headers)  # Send the request
    global token
    response_list = req.json()  # Convert to json format
    token = response_list['access_token']  # Pull the token from Spotify's response
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id,
                                                          client_secret=os.environ['SPOTIPY_CLIENT_SECRET'])
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    # Get users information using Spotipy and Spotify API
    headers = {'Authorization': 'Bearer ' + token}
    user = requests.get('https://api.spotify.com/v1/me', headers=headers)   # Get username from Spotify api
    resp = user.json()  # Convert to json format
    username = resp['id']
    playlists = sp.user_playlists(username)   # Use the username to get their playlists
    name_id = {}  # Then create a dict that has playlist name as key, playlist key as value
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
    request.session['token'] = token  # Save the token to the django session, can be retrieved later using get()
    return render(request, 'prune/choose.html', context)


# TODO: This function will get a refresh token to allow the user to close the tab and resume later
def refresh_token(request):
    return
