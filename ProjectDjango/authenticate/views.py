from django.shortcuts import render



def home(request):
    return render(request, 'authenticate/home.html')



def about(request):
    return render(request, 'authenticate/about.html')
