from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
import requests
import base64
import os

client_id = '0ffe4f5e083f464f8ad6061cd80785ca'
redirect_uri1 = 'http://ec2-18-191-18-199.us-east-2.compute.amazonaws.com/callback/'
redirect_uri2 = 'http://ec2-18-191-18-199.us-east-2.compute.amazonaws.com/about/'
token = 'NULL'


def home(request):
    HttpResponse('https://api.spotify.com/v1/artists/{3TVXtAsR1Inumwj472S9r4}')
    return render(request, 'authenticate/index.html')


def about(request):
    return render(request, 'authenticate/about.html')


def login(request):
    return redirect('https://accounts.spotify.com/authorize?client_id=' + client_id + '&response_type=code'
                    '&redirect_uri=' + redirect_uri1 + '&scope=user-read-private')


def callback(request):
    code = request.GET.get('code', '')
    if code == '':
        print("AN ERROR OCCURRED, REDIRECTING HOME")
        return render(request, 'authenticate/index.html')
    encoded = base64.b64encode((client_id + ':' + os.environ['SPOTIPY_CLIENT_SECRET']).encode('utf-8'))
    payload = {'grant_type': 'authorization_code', 'code': code, 'redirect_uri': redirect_uri2}
    r = requests.post('https://accounts.spotify.com/api/token',
                      headers={'Authorization', 'Basic ' + encoded.decode('utf-8')}, data=payload)
    return render(request, 'authenticate/about.html')


def refresh_token(request):
    return
