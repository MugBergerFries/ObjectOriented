from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
import json
import spotipy
import spotipy.util as util

client_id = '0ffe4f5e083f464f8ad6061cd80785ca'
redirect_uri = 'http://ec2-18-191-18-199.us-east-2.compute.amazonaws.com/about/'


def home(request):
    HttpResponse('https://api.spotify.com/v1/artists/{3TVXtAsR1Inumwj472S9r4}')
    return render(request, 'authenticate/index.html')


def about(request):
    return render(request, 'authenticate/about.html')


def login(request):
    return redirect('https://accounts.spotify.com/authorize?client_id=' + client_id + '&response_type=code'
                    '&redirect_uri=' + redirect_uri + '&scope=user-library-read')


def callback(request):
    return


def refresh_token(request):
    return
