from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse('<h1>Most important heading here</h1> <img src="data:image/jpeg;base64,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" alt="W3Schools.com" style="width:350px;height:197px;" style="width:50%;">')
