from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse('<img src="https://www.w3schools.com/images/w3schools_green.jpg" alt="W3Schools.com" style="width:104px;height:142px;">')
