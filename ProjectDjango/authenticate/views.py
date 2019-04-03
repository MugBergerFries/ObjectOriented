from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    HttpResponse('https://api.spotify.com/v1/artists/{3TVXtAsR1Inumwj472S9r4}')
    return render(request, 'authenticate/home.html')



def about(request):
    return render(request, 'authenticate/about.html')
