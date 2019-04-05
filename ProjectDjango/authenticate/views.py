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
    print("AT LOGIN\n")
    return redirect('https://accounts.spotify.com/authorize?client_id=' + client_id + '&response_type=code'
                    '&redirect_uri=' + redirect_uri1 + '&scope=user-read-private')


def callback(request):
    code = request.GET.get('code', '')
    print("AT CALLBACK, OS IS " + os.environ['SPOTIPY_CLIENT_SECRET'])
    if code == '':
        print("AN ERROR OCCURRED, REDIRECTING HOME")
        return render(request, 'authenticate/index.html')
    url = 'https://accounts.spotify.com/api/token'
    encoded = base64.b64encode("{}:{}".format(client_id, os.environ['SPOTIPY_CLIENT_SECRET']))#.encode('utf-8')).decode('utf-8')
    payload = {"grant_type": "authorization_code", "code": str(code), "redirect_uri": redirect_uri2}
    headers = {'Authorization': 'Basic ' + encoded}
    req = requests.post(url, data=payload, headers=headers)
    print(req.request.headers)
    print(req.request.body)
    print(req.text)
    return render(request, 'authenticate/about.html')


def refresh_token(request):
    return
