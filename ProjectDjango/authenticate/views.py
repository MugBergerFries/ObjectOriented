from django.shortcuts import render
from django.http import HttpResponse
import spotipy
import spotipy.util as util

def show_tracks(track_list):
    for i, item in enumerate(track_list['items']):
        track = item['track']
        print("   %d %32.32s %s" % (i, track['artists'][0]['name'], track['name']))

def home(request):
    username = '1236360620'
    #token = util.prompt_for_user_token(username, 'user-library-read')
    token = util.prompt_for_user_token(username,'user-library-read',client_id='0ffe4f5e083f464f8ad6061cd80785ca',client_secret='e1c15024a0c744a792d729510575a0ca',redirect_uri='http://ec2-18-191-18-199.us-east-2.compute.amazonaws.com/')
    if token:
        sp = spotipy.Spotify(auth=token)
        playlists = sp.user_playlists(username)
        for playlist in playlists['items']:
            if playlist['owner']['id'] == username:
                print(playlist['name'])
                print('  total tracks', playlist['tracks']['total'])
                results = sp.user_playlist(username, playlist['id'],
                                           fields="tracks,next")
                tracks = results['tracks']
                show_tracks(tracks)
                while tracks['next']:
                    tracks = sp.next(tracks)
                    show_tracks(tracks)
    else:
        print("Can't get token for", username)
    HttpResponse('https://api.spotify.com/v1/artists/{3TVXtAsR1Inumwj472S9r4}')
    return render(request, 'authenticate/home.html')



def about(request):
    return render(request, 'authenticate/about.html')
