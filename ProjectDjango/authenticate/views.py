from django.shortcuts import render
from django.http import HttpResponse
import spotipy
import spotipy.util as util


def test(request):
    return HttpResponse(<p1>Hi</p1>)


def home(request):
    HttpResponse('https://api.spotify.com/v1/artists/{3TVXtAsR1Inumwj472S9r4}')
    return render(request, 'authenticate/index.html')


def about(request):
    return render(request, 'authenticate/about.html')


def login(request):
    return render(request, 'authenticate/about.html')
