from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'authenticate/home.html')



def about(request):
    return HttpResponse('<h1>About our site: <h1>')
