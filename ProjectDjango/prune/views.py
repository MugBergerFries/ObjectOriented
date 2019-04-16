from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
import requests

client_id = '0ffe4f5e083f464f8ad6061cd80785ca'
redirect_uri1 = 'http://ec2-18-191-18-199.us-east-2.compute.amazonaws.com/magic/'

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
    test = request.GET.get('playlist')
    #print("ID HERE", test)
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
    #print("TOKEN: " + token)

    client_credentials_manager = SpotifyClientCredentials(client_id=client_id,
                                                          client_secret='e1c15024a0c744a792d729510575a0ca')
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # get users information
    headers = {'Authorization': 'Bearer ' + token}
    songs = requests.get('https://api.spotify.com/v1/playlists/'+test+'/tracks')
    resp = songs.json()
    print(resp)
    return render(request, 'prune/magic.html')
